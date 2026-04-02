from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.core.jwt import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token : str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    
    credentials_error = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )

    payload = decode_access_token(token)

    if payload is None:
        raise credentials_error
    
    user_id = payload.get("user_id")

    if user_id is None:
        return credentials_error
    user = db.query(User).filter(User.id == user_id).first()

    if user is None :
        return credentials_error
    
    return user
