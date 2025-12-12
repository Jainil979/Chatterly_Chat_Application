# 📘 Chatterly — Test Cases Documentation

**Version:** 2.0
**Maintainer:** Chatterly QA & Development Team
**Scope:** Unit Tests, Integration Tests, Security Tests, Performance Tests

---

## 📋 Overview

This document contains a comprehensive test plan for **Chatterly**, a real‑time chat application built with **Django, Django REST Framework, Channels, WebSockets, and end‑to‑end encryption**.

The goal of these test cases is to ensure:

* Full functional correctness
* Security and data protection
* Real‑time messaging reliability
* API compliance
* Performance under load

---

# 🧪 Unit Tests

Unit tests validate core components of **Accounts** and **Chat** apps.

---

## 🔐 Accounts App

### **Models — `test_models.py`**

**CustomUserModelTest**

* ✓ Create regular user
* ✓ Creating user without email raises error
* ✓ Create superuser with correct flags
* ✓ Email must be unique
* ✓ String representation correctness
* ✓ `get_full_name` returns expected value

### **Serializers — `test_serializers.py`**

**SignupSerializerTest**

* ✓ Valid signup data
* ✓ Missing fields validation
* ✓ Duplicate email detection
* ✓ Serializer creates user successfully

**LoginSerializerTest**

* ✓ Valid credentials authenticate
* ✓ Invalid credentials fail
* ✓ Non‑existent user login fails
* ✓ Inactive user login rejected

### **Authentication — `test_authentication.py`**

**CookieJWTAuthenticationTest**

* ✓ Valid token passes authentication
* ✓ No token → authentication fails
* ✓ Invalid/expired token → rejected

---

## 💬 Chat App

### **Models — `test_models.py`**

**ChatModelTests**

* ✓ Contact creation
* ✓ `ChatRoom.get_or_create_room` deterministic behavior
* ✓ Chat message creation with encryption + attachment

### **Serializers — `test_serializers.py`**

**SerializerTests**

* ✓ Contact serializer valid data
* ✓ AddUser serializer (valid case)
* ✓ Prevent adding yourself as contact (invalid case)

### **Strategies — `test_strategies.py`**

**StrategyTests**

* ✓ Text message strategy processing
* ✓ Typing indicator strategy
* ✓ Strategy factory returns correct handler
* ✓ Encryption + decryption flow

### **Observers — `test_observers.py`**

**ObserverTests**

* ✓ Observer registration
* ✓ Database log observer
* ✓ Notification observer
* ✓ Observer error isolation

---

# 🔗 Integration Tests

Integration tests verify interactions across multiple components.

## 🔐 Authentication Flow

* ✓ Signup → Login → Access authorized endpoint → Logout
* ✓ Password reset workflow
* ✓ Token refresh mechanisms
* ✓ Multi‑session token handling

## 💬 Chat Functionality

* ✓ Contact list API integration
* ✓ Add user flow
* ✓ Chat history retrieval
* ✓ Full message lifecycle (encrypt → send → decrypt)

---

# 🛡️ Security Tests

Security is mission‑critical for a chat application.

## 🔐 Authentication Security

* ✓ Password hashing validation
* ✓ JWT signature+expiration enforcement
* ✓ Cookie flags: **HttpOnly**, **Secure**, **SameSite=None**
* ✓ SQL injection prevention (ORM)

## 💬 Chat Security

* ✓ Encryption key must be 32 bytes
* ✓ End‑to‑end encryption success tests
* ✓ XSS sanitization for message content

---

# 🚀 Performance Tests

## Basic Performance

* ✓ Bulk user creation under constraints
* ✓ Login performance under load
* ✓ Query optimization using `select_related` and `prefetch_related`

---

# 📊 Test Coverage Summary

## Models Coverage

| Model       | Coverage |
| ----------- | -------- |
| CustomUser  | 100%     |
| Profile     | 90%      |
| Contact     | 100%     |
| ChatRoom    | 100%     |
| ChatMessage | 100%     |

## API Endpoints Coverage

| Component          | Coverage |
| ------------------ | -------- |
| Authentication     | 95%      |
| Chat APIs          | 85%      |
| WebSocket handlers | 85%      |

## Critical Paths

* User Registration: **Complete**
* Login/Logout: **Complete**
* Message Sending: **Complete**
* Contact Management: **Complete**
* File Uploads: **Partial** (ongoing improvements)

---

# 🧰 Test Commands

### Run All Tests

```bash
python manage.py test
pytest --cov=.
```

### Run Specific Apps

```bash
python manage.py test accounts
python manage.py test chat
```

### Run With Coverage Report

```bash
pytest --cov=accounts --cov-report=html
pytest --cov=chat --cov-report=html
```

### Run Specific Test Files

```bash
python manage.py test accounts.tests.test_models
python manage.py test chat.tests.test_views
```

---

# 🎯 Key Test Scenarios (High‑Level)

## User Registration

* Valid registration
* Duplicate email prevention
* Password strength enforcement

## User Authentication

* JWT token generation
* Token refresh logic
* Cookie‑based authentication flow

## Chat Features

* Contact add/remove
* Encrypted message sending
* Real-time WebSocket messaging
* File attachment tests

## Error Handling

* Invalid inputs
* Unauthorized access
* Network interruption handling
* Graceful DB error responses

---

# 📝 Notes

* Uses Django’s `TestCase` for database isolation
* Factories used for test data generation
* External services mocked
* Async WebSocket tests use **pytest‑asyncio**
* Coverage via **pytest‑cov**

---

# 🔄 Continuous Testing

Automatic test execution occurs on:

* Every pull request
* Every push to `main`
* CI pipeline (GitHub Actions recommended)

---

# ✅ Conclusion

This test suite ensures Chatterly remains secure, scalable, and reliable under real‑world usage conditions.

*If you want, I can also generate a full `tests/` folder structure with template files for quick integration.*
