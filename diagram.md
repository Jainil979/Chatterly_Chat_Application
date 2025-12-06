# Chatterly — Diagrams

This file contains GitHub-friendly Mermaid diagrams for the Chatterly chat application. The previous parse error was caused by using `<<interface>>` annotation inside class declarations, which GitHub's Mermaid parser does not accept. The diagrams below avoid that syntax and render correctly on GitHub.

---

## Class Diagram

```mermaid
classDiagram
    direction LR

    class CustomUser {
        +id: UUID
        +email: str
        +is_active: bool
        +get_full_name()
    }

    class Profile {
        +display_name: str
        +avatar_url: str
        +bio: str
    }

    class Contact {
        +owner_id: UUID
        +contact_user_id: UUID
        +created_at: datetime
    }

    class ChatRoom {
        +id: UUID
        +room_type: str
        +get_or_create_room(user_a, user_b)
    }

    class ChatMessage {
        +id: UUID
        +room_id: UUID
        +sender_id: UUID
        +cipher_text: str
        +attachment_url: str
        +created_at: datetime
    }

    class Attachment {
        +id: UUID
        +file_url: str
        +content_type: str
    }

    class PresenceRepository {
        +set_online(user_id)
        +set_offline(user_id)
        +get_online_users()
    }

    class Repositories {
        +ChatRoomRepository
        +ChatMessageRepository
        +ContactRepository
    }

    class MessageHandler {
        +can_handle(data)
        +process(data, room, user)
    }

    class EncryptionStrategy {
        +encrypt(plaintext, key)
        +decrypt(ciphertext, key)
    }

    class EventManager {
        +add_observer(obs)
        +notify_all(event_type, data)
    }

    class Observer {
        +should_handle(event_type, data)
        +notify(event_type, data)
    }

    class WebSocketConsumer {
        +connect()
        +disconnect()
        +receive_json(data)
    }

    CustomUser <|-- Profile
    CustomUser "1" <-- "*" Contact : owns
    CustomUser "1" <-- "*" ChatMessage : sends
    ChatRoom "1" <-- "*" ChatMessage : contains
    ChatRoom "*" <-- "*" CustomUser : participants
    ChatMessage o-- Attachment : may have

    WebSocketConsumer --> MessageHandler : uses
    WebSocketConsumer --> EventManager : notifies
    MessageHandler ..> EncryptionStrategy : uses

    Repositories -- ChatRoom
    Repositories -- ChatMessage
    Repositories -- Contact
    PresenceRepository ..> Repositories : reads
    EventManager ..> Observer : manages
```

---

## Sequence Diagram (Message Flow)

```mermaid
sequenceDiagram
    participant Client
    participant Server as ASGI/Daphne
    participant Consumer as WebSocketConsumer
    participant Handler as MessageHandler
    participant Repo as ChatMessageRepository
    participant Redis as ChannelLayer/Redis
    participant Event as EventManager

    Client->>Server: WebSocket send message (JSON)
    Server->>Consumer: route to ChatConsumer.receive_json
    Consumer->>Handler: handler = factory.get_handler(data)
    Handler-->>Consumer: processed_payload
    Consumer->>Repo: create_message(processed_payload)
    Repo-->>Consumer: message instance
    Consumer->>Redis: channel_layer.group_send(broadcast)
    Consumer->>Event: notify_all('message_created', payload)
    Event->>Observer: send notifications / logs
    Redis-->>Client: broadcast to other participants
```

---

