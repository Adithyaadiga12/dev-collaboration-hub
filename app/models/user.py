from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
# → inherits from Base — this is what makes it a DB table, not just a class

    __tablename__ = "users"
    # → the actual table name in SQLite

    id = Column(Integer, primary_key=True, index=True)
    # → every row gets a unique id automatically
    # → index=True makes lookups by id faster

    username = Column(String, unique=True, nullable=False)
    # → unique=True → no two users can have the same username
    # → nullable=False → this field is required, can't be empty

    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    # → we NEVER store the real password — only its hash
    # → even if DB is hacked, passwords are safe
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, server_default=func.now())
    # → automatically saves the timestamp when a user is created