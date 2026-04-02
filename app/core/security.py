from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


#**Why hash passwords?**

#If your database gets hacked and passwords are stored as plain text — every user's account everywhere is compromised (people reuse passwords). A hash is a one-way transformation:

#"mypassword123"  →  hash()  →  "$2b$12$abc...xyz"

    # You CANNOT reverse it:
#"$2b$12$abc...xyz"  →  reverse?  →  ❌ impossible