from fastapi import FastAPI
from . import models
from .database import engine
from blog.routers import post, user, auth
from .oauth2 import oauth2_scheme

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
    },
    {
        "name": "Posts",
        "description": "Handles the **blog post** logic"
    }
]

app = FastAPI(description=description, title="My Test API", openapi_tags=tags_meta)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

