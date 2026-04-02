from datetime import datetime, timedelta
from jose import JWTError, jwt

# This is your secret key — the "secret recipe" only your server knows
# In real projects this lives in a .env file, never hardcoded
SECRET_KEY = "9c5aebb835352920816571e77ee104cb1de8d77449d9aaa1fc98d7e42516d9bd"

# The algorithm used to sign the token
ALGORITHM = "HS256"

# How long the token lives before expiring
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict) -> str:
    # Make a copy of the data so we don't modify the original
    payload = data.copy()

    # Calculate the expiry time
    # datetime.utcnow() = current time
    # timedelta() = adds 30 minutes to it
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Add expiry to the payload
    # "exp" is a standard JWT key — jose library understands it automatically
    payload.update({"exp": expire})

    # Create and return the token
    # jwt.encode() takes payload + secret key + algorithm → returns token string
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token

def decode_access_token(token:str) -> dict:
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
    