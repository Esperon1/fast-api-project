from fastapi import FastAPI, Request, Depends, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from .database import get_db

from . import models
from .database import engine
from .routers import posts, users, auth, votes
from .config import Settings

settings = Settings()

# create the tables. Since the table is already created, this line will have no effect
models.Base.metadata.create_all(bind=engine)

app = FastAPI()  # main application instance

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(posts.router, tags=["Posts"])
app.include_router(users.router, tags=["Users"])
app.include_router(auth.router, tags=["Authentication"])

app.include_router(votes.router, tags=["Votes"])


@app.get("/", response_class=HTMLResponse)
def get_user_page(request: Request,
                  db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    theme = request.cookies.get("theme", "light")

    return templates.TemplateResponse(
        "users.html",
        {
            "request": request,
            "users": users,
            "theme": theme
        }
    )


@app.get("/toggle-theme")
def toggle_theme(request: Request):
    current_theme = request.cookies.get("theme", "light")
    new_theme = "dark" if current_theme == "light" else "light"

    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="theme", value=new_theme)
    return response
