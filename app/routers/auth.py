from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse,LoginRequest,TokenResponse
from app.core.security import hash_password,verify_password
from app.core.jwt import create_access_token



# APIRouter is like a mini-app — groups related routes together
# We'll plug this into main.py
router = APIRouter(
    prefix="/auth",      # all routes here start with /auth
    tags=["Authentication"]  # groups them in /docs
)

@router.post("/register", response_model=UserResponse, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Step 1: Check if email already exists
    #similar to : SELECT * FROM users WHERE email = "adi@gmail.com" LIMIT 1;    
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Step 2: Check if username already exists
    existing_username = db.query(User).filter(User.username == user_data.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")

    # Step 3: Hash the password — never store plain text
    hashed = hash_password(user_data.password)

    # Step 4: Create the User object
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed
    )

    # Step 5: Save to database
    db.add(new_user)       # stage the new user
    db.commit()            # actually write to DB (like hitting Save)
    db.refresh(new_user)   # reload from DB to get the auto-generated id

    return new_user

@router.post("/login",response_model=TokenResponse)
def login(login_data: LoginRequest,db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
 #it is good practice to use the same error message for both cases (security reasons)

    token = create_access_token(data={"user_id": user.id})\
    
    return {"access_token": token, "token_type": "bearer"}

          