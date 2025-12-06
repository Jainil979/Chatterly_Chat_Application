# 🚀 Chatterly - Real-time Chat Application

<div align="center">
  <img src="https://img.shields.io/badge/Django-5.2.3-green?style=for-the-badge&logo=django" alt="Django"/>
  <img src="https://img.shields.io/badge/Django%20Channels-4.2.2-blue?style=for-the-badge&logo=django" alt="Django Channels"/>
  <img src="https://img.shields.io/badge/WebSocket-Chat-orange?style=for-the-badge&logo=websocket" alt="WebSocket"/>
  <img src="https://img.shields.io/badge/PostgreSQL-15-blue?style=for-the-badge&logo=postgresql" alt="PostgreSQL"/>
  <img src="https://img.shields.io/badge/Redis-7-red?style=for-the-badge&logo=redis" alt="Redis"/>
</div>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-local-development">Local Dev</a> •
  <a href="#-contributing">Contributing</a>
</p>

---

## ✨ Features

### 🎯 Core

* Real-time messaging using **WebSockets** (Django Channels)
* JWT-based authentication stored securely in **HttpOnly** cookies
* 1:1 & group chat rooms, message history (infinite scroll)
* Typing indicators, read receipts, user presence (online/offline)
* File attachments (uploads), user profiles with avatars

### 🔒 Security

* JWT + refresh tokens (Simple JWT)
* CSRF protection & secure cookie flags
* Rate limiting for sensitive endpoints (recommended to enable)
* XSS/SQL protections via Django best practices

### 📱 Frontend

* Responsive UI (Tailwind CSS)
* Real-time UI updates, toast notifications, dark/light mode

---

## 🛠 Tech Stack

**Backend**

* Django 5.2.3, Django REST Framework
* Django Channels 4.2.2 + Daphne (ASGI)
* PostgreSQL (primary DB)
* Redis (channel layer / caching)
* WhiteNoise or S3 (static/media)

**Frontend**

* Tailwind CSS, Vanilla JS, Alpine.js (optional for small reactive bits)

**Dev / Ops**

* Render.com (example), GitHub Actions (CI), Docker (optional)

---

## 🚀 Quick Start

### Prerequisites

* Python 3.11+
* PostgreSQL 15+
* Redis 7+
* Git

### Clone & install

```bash
git clone https://github.com/your-username/chatterly.git
cd chatterly

python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Edit .env and fill values (do NOT commit secrets)
```

### Database & static files

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### Run (development)

```bash
# Development HTTP + WebSocket (Daphne integrates with runserver)
python manage.py runserver
# or run Channels worker in separate terminal if needed:
python manage.py runworker
```

Visit: `http://localhost:8000`

---

## ⚙️ Local development

### PostgreSQL (example Ubuntu)

```bash
sudo apt install postgresql postgresql-contrib
sudo -u postgres psql
# inside psql:
CREATE DATABASE chatterly;
CREATE USER chatter_user WITH PASSWORD 'strong_password';
GRANT ALL PRIVILEGES ON DATABASE chatterly TO chatter_user;
\q
```

### Redis (example Ubuntu)

```bash
sudo apt install redis-server
sudo systemctl enable --now redis
redis-cli ping   # should return PONG
```

### Useful commands

```bash
# Make & apply new migrations
python manage.py makemigrations
python manage.py migrate

# Run tests
python manage.py test
# or with coverage
pytest --cov=.
```

---

## 🌐 Deployment

This repo works well on Render, Heroku, or a Docker/Kubernetes setup. For WebSockets use **Daphne** (ASGI) on the web service and run a background worker for Channels consumers.

### Render (high level)

1. Create a Render Web Service — connect repo.
2. Create managed Postgres & Redis (Render can provision).
3. Add required environment variables (see below).
4. Build command:

```bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
```

5. Start command (Daphne):

```bash
daphne -b 0.0.0.0 -p $PORT chatterly.asgi:application
```

6. Create a Background Worker with:

```bash
python manage.py runworker
```

> If you do not require WebSockets, you may use Gunicorn for HTTP only:

```bash
gunicorn chatterly.wsgi:application --bind 0.0.0.0:$PORT
```

### Important environment variables

Set these securely in your host (Render UI, or env file on server):

```
DEBUG=False
SECRET_KEY=replace-with-strong-random-secret
ALLOWED_HOSTS=your-app.onrender.com,example.com
DATABASE_URL=postgres://user:pass@host:port/dbname
REDIS_URL=redis://:password@host:port
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=you@example.com
EMAIL_HOST_PASSWORD=app-password
AWS_ACCESS_KEY_ID=...            # if using S3
AWS_SECRET_ACCESS_KEY=...        # if using S3
AWS_STORAGE_BUCKET_NAME=...      # if using S3
```

**Note:** Never commit `.env` or secrets to source control.

---

## 📁 Project structure (high level)

```
chatterly/
├── accounts/            # authentication, custom user model
├── chat/                # models, consumers, repositories, strategies
├── core/                # health checks, static pages
├── chatterly/           # project settings, ASGI & WSGI
├── static/              # frontend static assets
├── media/               # user uploads (use S3 in prod)
├── requirements.txt
├── render.yaml
├── .env.example
└── README.md
```

---

## 🔧 Environment variables (example `.env.example`)

```env
# Django
DEBUG=True
SECRET_KEY=your-secret-key

# Database (local)
DB_NAME=chatterly
DB_USER=chatter_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# For DATABASE_URL (preferred)
DATABASE_URL=postgres://user:password@localhost:5432/chatterly

# Redis
REDIS_URL=redis://localhost:6379/0

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=you@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=you@gmail.com
```

---

## 🔐 Authentication

Chatterly uses JWT tokens (Simple JWT). The recommended flow:

1. `POST /api/register/` — Create account
2. `POST /api/login/` — Receive access & refresh tokens set as HttpOnly cookies
3. Protected endpoints read the access token from cookies
4. `POST /api/token/refresh/` — Refresh access token using refresh cookie
5. `POST /api/logout/` — Clear cookies & blacklist refresh token

Example JS fetch (send cookies automatically):

```js
fetch('/api/rooms/', {
  method: 'GET',
  credentials: 'include'
});
```

---

## 💬 Real-time features

### WebSocket endpoints

* `ws://your-domain/ws/chat/<room_id>/` — chat room connection
* `ws://your-domain/ws/notifications/` — user notifications

### Typical event (JSON)

```json
{
  "type": "chat_message",
  "message": "Hello world!",
  "user": "alice",
  "timestamp": "2025-01-01T12:00:00Z"
}
```

Supported events:

* `chat_message`, `user_joined`, `user_left`, `typing`, `message_read`

---

## 📦 API reference (short)

### Authentication

| Method |              Endpoint | Description             |
| ------ | --------------------: | ----------------------- |
| POST   |      `/api/register/` | Register new user       |
| POST   |         `/api/login/` | Login & set JWT cookies |
| POST   |        `/api/logout/` | Logout user             |
| POST   | `/api/token/refresh/` | Refresh access token    |

### Chat

| Method |                    Endpoint | Description  |
| ------ | --------------------------: | ------------ |
| GET    |               `/api/rooms/` | List rooms   |
| POST   |               `/api/rooms/` | Create room  |
| GET    | `/api/rooms/{id}/messages/` | Get messages |
| POST   |            `/api/messages/` | Send message |

### Users

| Method |                  Endpoint | Description    |
| ------ | ------------------------: | -------------- |
| GET    |             `/api/users/` | List users     |
| GET    |        `/api/users/{id}/` | Get profile    |
| PUT    |        `/api/users/{id}/` | Update profile |
| POST   | `/api/users/{id}/avatar/` | Upload avatar  |

---

## 🤝 Contributing

We welcome contributions — small or large!

**How to contribute**

1. Fork the repo
2. Create a branch: `git checkout -b feat/your-feature`
3. Implement & test changes
4. Add tests and update docs
5. Open a pull request and describe the changes

**Coding standards**

* Follow PEP8 & type hints when possible
* Write unit tests for new features
* Keep PRs small & focused

---

## 🧪 Testing

Run tests:

```bash
python manage.py test
# or
pytest
```

Generate coverage:

```bash
pytest --cov=.
```

---

## 🙏 Acknowledgments

Thanks to the open-source ecosystem: Django, Django Channels, Daphne, Postgres, Redis, Tailwind CSS — and to the contributors Jainil & Paras for building Chatterly.

<div align="center">
  <p>Made with ❤️ by Jainil & Kalrav & Akshay </p>
  <p>
    <a href="https://github.com/your-username/chatterly">GitHub</a>
  </p>
</div>

---

*If you’d like, I can :*

* format this into a ready-to-commit `README.md` in your repo,
* add a short `getting-started` script, or
