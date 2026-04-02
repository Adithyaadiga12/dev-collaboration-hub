from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, users, projects, chat, github
from app.models import user, project

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Dev Collaboration Hub",
    description="A platform for developers to collaborate on projects",
    version="1.0.0"
)

# Add this CORS middleware ↓
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(chat.router)
app.include_router(github.router)

@app.get("/")
def home():
    return {"message": "Welcome to Dev Collaboration Hub!"}

@app.get("/health")
def health_check():
    return {"status": "Server is running fine!"}


## 🧠 What is CORS?

#CORS (Cross Origin Resource Sharing) is a browser security rule:

#Your HTML file is at:  file:///C:/Adithya/test_chat.html
#Your server is at:     http://localhost:8000

#Different origins → browser blocks it by default