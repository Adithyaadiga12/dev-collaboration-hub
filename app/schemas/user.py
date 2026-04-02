from pydantic import BaseModel
#pydantic for data validation and serialization
# This defines what the INCOMING registration request must look like
# If any field is missing → FastAPI auto-rejects with 422 error
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

# This defines what we send BACK after registration
# Notice: no password field — we never send passwords back
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True  # allows converting SQLAlchemy object → Pydantic

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str