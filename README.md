# Dev Collaboration Hub 🚀

A backend API for developers to find projects, collaborate with teams, and chat in real time.

Built this to learn backend development properly — not by following a tutorial, but by understanding every single concept from scratch.

## What It Does

- **Sign up and log in** securely with JWT tokens
- **Create projects** and look for collaborators
- **Chat in real time** with your project team
- **Link your GitHub repo** and see live stats — stars, forks, language, last updated

## Tech Stack

| What | Why |
|---|---|
| FastAPI | Fast, modern Python web framework |
| SQLite + SQLAlchemy | Database with Python ORM |
| JWT + bcrypt | Secure auth without storing plain passwords |
| WebSockets | Real-time chat without page refresh |
| httpx | Calling GitHub's API from our backend |

## How It's Structured
```
app/
├── main.py              → Entry point, plugs everything together
├── database.py          → Database connection and session management
├── core/
│   ├── security.py      → Password hashing with bcrypt
│   ├── jwt.py           → Token creation and verification
│   └── dependencies.py  → Reusable route protection
├── models/              → Database table definitions
├── schemas/             → Request and response shapes
└── routers/             → All API endpoints
    ├── auth.py          → Register and login
    ├── users.py         → User profile
    ├── projects.py      → Project CRUD
    ├── chat.py          → WebSocket chat
    └── github.py        → GitHub API integration
```

## API Endpoints
```
POST   /auth/register              → Create account
POST   /auth/login                 → Login, get JWT token
GET    /users/me                   → Your profile
GET    /users/all                  → All registered users
POST   /projects/                  → Create a project
GET    /projects/                  → Browse all projects
GET    /projects/{id}              → View one project
PUT    /projects/{id}              → Edit your project
DELETE /projects/{id}              → Delete your project
WS     /ws/{project_id}/{username} → Join project chat room
GET    /projects/{id}/github       → Live GitHub repo stats
```

## Running It Locally
```bash
git clone https://github.com/Adithyaadiga12/dev-collab-hub.git
cd dev-collab-hub
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/docs` to explore all endpoints interactively.

## Things I Learned Building This

- How JWT authentication actually works under the hood
- Why passwords should never be stored as plain text
- The difference between authentication and authorization
- How WebSocket connections differ from regular HTTP
- How to call external APIs from your own backend
- How dependency injection keeps code clean and reusable

## What's Next

- [ ] Frontend with React
- [ ] Switch SQLite to PostgreSQL
- [ ] Deploy on Railway or Render
- [ ] Add email notifications when someone joins your project

---

Built by **Adithya Adiga H S** · [LinkedIn](https://linkedin.com/in/adithyaadiga12) · [GitHub](https://github.com/Adithyaadiga12)   