from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer,primary_key=True ,index = True)
    title = Column(String,nullable = False)
    description = Column(String,nullable = True)
    github_url = Column(String,nullable=True)
    is_open = Column(Boolean,default= True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner_id = Column(Integer,ForeignKey("users.id"),nullable = False)
    owner = relationship("User", backref="projects")
    # → this is SQLAlchemy magic — not a real column in the DB
    # → it creates two shortcuts:

    # Shortcut 1: project.owner
    # → gives you the full User object of whoever owns this project
    # → no extra SQL needed

    # Shortcut 2: user.projects (the "backref" part)
    # → gives you all projects belonging to a user
    # → again, no extra SQL needed

