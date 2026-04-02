from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# This is the path to our SQLite database file
# It will be created automatically when we run the app
DATABASE_URL = "sqlite:///./dev_collab.db"

# The engine is the actual connection to the database
# connect_args is needed only for SQLite (not for PostgreSQL/MySQL)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# SessionLocal is a factory — every time we need to talk to
# the DB, we create a new session from this factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the parent class all our database models will inherit from
# It's what connects our Python classes to actual DB tables
Base = declarative_base()

# This is a "dependency" — a reusable function that gives any
# route a fresh DB session and closes it when the request is done
def get_db():
    db = SessionLocal()    # open a session (like opening Excel)
    try:
        yield db           # give it to whoever asked for it
    finally:
        db.close()         # always close it after the request ends