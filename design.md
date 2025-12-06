# Chatterly — Design Patterns Implementation

**Version:** 2.0
**Maintainer:** Chatterly Development Team

---

## 🌟 Overview

This document describes the integration of three core design patterns into **Chatterly** (a Django-based chat application): **Repository**, **Strategy**, and **Observer**. The goal is improved maintainability, testability, and separation of concerns while preserving existing APIs and functionality.

Key guiding principles:

* **SOLID** principles (SRP, OCP, ISP, DIP)
* **Separation of concerns** — patterns target specific responsibilities
* **Backward compatibility** — keep current APIs unchanged
* **Progressive adoption** — patterns can be introduced incrementally

---

## 🏗️ Architecture Overview

### Before (simplified)

```
Django Views
  └─ direct ORM calls
```

### After (with patterns)

```
Django Views/APIViews
  └─ Repository Layer (ChatRoomRepo, ChatMessageRepo, ContactRepo, PresenceRepo)
       └─ Django ORM
WebSocket Consumers
  └─ Strategy (MessageHandlers) + Observer (EventManager and Observers)
       └─ Repository Layer & Redis/Channel Layer
```

This separation centralizes data access, isolates message processing logic, and decouples side-effects (notifications, analytics, logs).

---

## 🎯 Implemented Patterns — Rationale & Location

| Pattern    | Problem solved                                         | Implementation file             |
| ---------- | ------------------------------------------------------ | ------------------------------- |
| Repository | Scattered ORM usage; hard to test                      | `repositories.py`               |
| Strategy   | Multiple message types with different handling logic   | `strategies.py`                 |
| Observer   | Many side effects (notifications, logs) tied to events | `observers.py`, `event_manager` |

---

## 📦 Repository Pattern

**Purpose:** Provide an abstraction over data persistence to centralize queries, caching, and business rules.

### Base repository (interface)

```py
from abc import ABC, abstractmethod
from typing import Any

class BaseRepository(ABC):
    @abstractmethod
    def get_by_id(self, pk: int) -> Any:
        raise NotImplementedError

    @abstractmethod
    def filter(self, **kwargs):
        raise NotImplementedError
```

### Example: ChatRoomRepository

```py
class ChatRoomRepository(BaseRepository):
    def __init__(self, model):
        self.model = model

    def get_or_create_room(self, user_a, user_b):
        # Ensure deterministic ordering
        if user_a.id > user_b.id:
            user_a, user_b = user_b, user_a
        room, _ = self.model.objects.get_or_create(user_a=user_a, user_b=user_b)
        return room
```

### Example: ChatMessageRepository

```py
class ChatMessageRepository(BaseRepository):
    def __init__(self, model):
        self.model = model

    def create_message(self, room, sender, cipher: str = '', attachment=None, attachment_url=None):
        return self.model.objects.create(
            room=room,
            sender=sender,
            cipher=cipher,
            attachment=attachment,
            attachment_url=attachment_url
        )
```

### Example: PresenceRepository (Redis-backed)

```py
class PresenceRepository:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.online_key = 'online_users'

    def set_online(self, user_id: int):
        self.redis.sadd(self.online_key, user_id)

    def get_online_users(self):
        return {int(x) for x in self.redis.smembers(self.online_key)}
```

### Usage in views

```py
# Before
qs = Contact.objects.filter(owner=request.user)

# After
contact_repo = ContactRepository()
contacts = contact_repo.get_user_contacts(request.user)
```

**Benefits:** testability (mock repos), centralized caching and query logic, consistent patterns for DB access.

---

## 🎮 Strategy Pattern

**Purpose:** Encapsulate different message-processing algorithms so they are interchangeable and extensible.

### Encryption strategy interface

```py
from abc import ABC, abstractmethod

class EncryptionStrategy(ABC):
    @abstractmethod
    def encrypt(self, plaintext: str, key: bytes) -> str:
        pass

    @abstractmethod
    def decrypt(self, ciphertext: str, key: bytes) -> str:
        pass
```

### Concrete example (NaCl SecretBox)

```py
from nacl.secret import SecretBox
import base64

class SecretBoxEncryptionStrategy(EncryptionStrategy):
    def encrypt(self, plaintext: str, key: bytes) -> str:
        box = SecretBox(key)
        cipher = box.encrypt(plaintext.encode())
        return base64.b64encode(cipher).decode()

    def decrypt(self, ciphertext: str, key: bytes) -> str:
        box = SecretBox(key)
        data = base64.b64decode(ciphertext)
        return box.decrypt(data).decode()
```

### MessageHandler strategy interface

```py
class MessageHandler(ABC):
    @abstractmethod
    def can_handle(self, data: dict) -> bool:
        pass

    @abstractmethod
    def process(self, data: dict, room, user, encryption_strategy) -> dict:
        pass
```

### Concrete handlers

* `TextMessageHandler` — encrypts and stores text messages
* `AttachmentMessageHandler` — stores attachment metadata
* `TypingIndicatorHandler` — handles typing events

### Factory

A factory returns the first handler that `can_handle` the incoming payload. This eliminates long conditional blocks and allows adding new handlers with minimal impact.

### Usage in Consumer

```py
handler = message_handler_factory.get_handler(data)
if handler:
    processed = handler.process(data, self.room, user, self.encryption)
    if processed['type'] == 'text':
        msg = await database_sync_to_async(self.message_repo.create_message)(
            self.room, user, cipher=processed['cipher']
        )
```

**Benefits:** open for extension, closed for modification; easy to test each handler independently.

---

## 👁️ Observer Pattern

**Purpose:** Decouple producers of events (e.g., message creation) from consumers (notifications, logs, analytics).

### EventObserver interface

```py
class EventObserver(ABC):
    @abstractmethod
    def should_handle(self, event_type: str, data: dict) -> bool:
        pass

    @abstractmethod
    def notify(self, event_type: str, data: dict):
        pass
```

### Example Observers

* `DatabaseLogObserver` — persists event logs for analytics
* `NotificationObserver` — sends push/FCM notifications
* `ContactSyncObserver` — syncs contacts across devices
* `ReadReceiptObserver` — handles read receipts

### EventManager (Singleton)

```py
class EventManager:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._observers = []
            cls._instance._initialize_observers()
        return cls._instance

    def _initialize_observers(self):
        self.add_observer(DatabaseLogObserver())
        self.add_observer(NotificationObserver())
        # ...

    def add_observer(self, obs):
        self._observers.append(obs)

    def notify_all(self, event_type: str, data: dict):
        for observer in self._observers:
            try:
                if observer.should_handle(event_type, data):
                    observer.notify(event_type, data)
            except Exception as e:
                # fail-safe: log and continue
                print(f"Observer error: {e}")
                continue
```

### Typical events

* `message_created`, `typing_event`, `user_presence`, `message_read`, `message_delivered`, `contact_added`, `contact_removed`

### Usage

In an async consumer:

```py
await sync_to_async(self.event_manager.notify_all)(
    'message_created',
    { 'message_id': msg.id, 'room_id': self.room.id, 'sender_id': user.id, ... }
)
```

**Benefits:** loose coupling, easy integration of new side-effects, scalable when observers are made async.

---

## 🔗 How patterns interact (flow)

**Incoming WebSocket message**

```
WebSocket -> Strategy (determine type) -> Repository (persist) -> WebSocket broadcast -> EventManager.notify_all() -> Observers act
```

**HTTP request**

```
HTTP -> Django View -> Repository -> Response
```

---

## 📁 Project File Structure (recommended)

```
chat/
├─ consumers.py        # WebSocket consumers (uses strategies & observers)
├─ models.py
├─ repositories.py     # repository implementations
├─ strategies.py       # message handlers & encryption strategies
├─ observers.py        # observer implementations & EventManager
├─ serializers.py
├─ views.py            # views using repositories
├─ tests/
│  ├─ test_repositories.py
│  ├─ test_strategies.py
│  └─ test_observers.py
```

---

## ✅ Benefits & Trade-offs

**Benefits achieved**

* Testability: mock repositories and isolated strategies
* Maintainability: single responsibility components
* Extensibility: add new message types and observers easily

**Trade-offs / Considerations**

* Added complexity and learning curve for new developers
* Potential performance costs (mitigable via caching, async observers)
* Requires clear documentation and tests

---

## 🚀 Usage Examples (short)

1. **Add new message type**

   * Create handler in `strategies.py`
   * Register it in factory
   * Add tests

2. **Add new observer**

   * Implement `EventObserver`
   * Register in `EventManager`

3. **Use repository in view**

```py
contact_repo = ContactRepository()
contacts = contact_repo.get_user_contacts(request.user)
```

---

## 🔮 Future extensions

* CQRS + event sourcing for better read/write separation
* Mediator for complex interaction orchestration
* Decorator for cross-cutting concerns (logging, caching)
* Chain of Responsibility for validation pipelines

---

## 🛠️ Development guidelines & checklist

* Use repositories for DB operations where business logic exists
* Use strategies for varying algorithms and message types
* Use observers for side effects and integrations
* Keep observers async for heavy tasks
* Add unit tests for every repository/strategy/observer

---

## 🤝 Contributing

1. **New repository**: extend `BaseRepository`, add tests, document behavior
2. **New strategy**: implement `MessageHandler`, add to factory, add tests
3. **New observer**: implement `EventObserver`, register in `EventManager`, add tests

---

## 🏁 Conclusion

Applying Repository, Strategy, and Observer patterns in Chatterly increases maintainability, testability, and extensibility. Adopt incrementally and accompany each change with tests and documentation.

---

*If you'd like, I can also generate individual starter files for `repositories.py`, `strategies.py`, and `observers.py` with skeleton code and basic tests.*
