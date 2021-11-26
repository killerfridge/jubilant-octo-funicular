from jose import JWTError, jwt
from datetime import timedelta, datetime
from fastapi import Depends, status, HTTPException
from . import schemas
from fastapi.security import OAuth2PasswordBearer
from . import database, models
from sqlalchemy.orm import Session
from .config import settings
import os


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key


# SECRET KEY
# Should be stored as an environment variable
# SECRET_KEY = "b394e4fac2c6abda64846ac9bc21b2c71cc2e41dc0589bb59685751a64c4d2c5"

# Algorithm
ALGORITHM = settings.algorithm
# Expiration time
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp": expire
    })

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if not user_id:
            raise credentials_exception
        token_data = schemas.TokenData(id=user_id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials",
                                          headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
