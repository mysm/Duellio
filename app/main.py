# app/main.py
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.api.routers import main_router
from app.core.config import settings

app = FastAPI(title=settings.app_title, description=settings.description)

app.include_router(main_router)

add_pagination(app)
