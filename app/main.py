from fastapi import FastAPI

from . import models
from .database import engine

from .routers import posts, users, auth, votes
from .config import Settings

# Varifying Environment Variables

settings = Settings()

# create the tables. Since the table is already created, this line will have no effect
models.Base.metadata.create_all(bind=engine)

app = FastAPI()  # main application instance

app.include_router(posts.router, tags=["Posts"])
app.include_router(users.router, tags=["Users"])
app.include_router(auth.router, tags=["Authentication"])

app.include_router(votes.router, tags=["Votes"])
