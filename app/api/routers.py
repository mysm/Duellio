from fastapi import APIRouter

from app.api.endpoints import (
    situations_router,
    tags_router,
)

main_router = APIRouter()
main_router.include_router(
    situations_router, prefix="/situations", tags=["Situations"]
)
main_router.include_router(
    tags_router, prefix="/tags", tags=["Tags"]
)
