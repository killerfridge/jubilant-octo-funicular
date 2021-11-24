from fastapi import FastAPI, status, Response, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from . import models
from .database import engine, get_db
from .schemas import PostCreate, Post, User, UserCreate, UserValidate, UserAll
from sqlalchemy.orm import Session
from typing import List
from blog.routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

# asdf = "hello"

description = """
## Test API
This is the test API that we are building to try and get to grips with how FastAPI works.

We want to implement user based roles, JWT authentication, and some basic CRUD activity"""

users_description = """
Operations with the users.
The **login** logic is also here.
"""

tags_meta = [
    {
        "name": "Users",
        "description": users_description
    },
    {
        "name": "Authentication",
        "description": "Handles all the **authentication** logic"
    }
]

app = FastAPI(description=description, title="My Test API", openapi_tags=tags_meta)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.post('/token', tags=['Security'])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username or password incorrect")

    if not user.check_password(form_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username or password incorrect")

    return {"access_token": user.username, 'token_type': 'bearer'}
