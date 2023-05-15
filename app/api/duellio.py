# app/api/duellio.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.duellio import (
    create_situation,
    get_situation_id_by_name,
    read_all_situations_from_db,
    read_all_situations_with_tags_from_db
)
from app.schemas.duellio import Situation, SituationDB, SituationSchemaDB

router = APIRouter()


@router.get(
    "/situation",
    response_model=list[SituationSchemaDB],
    response_model_exclude_none=True,
)
async def get_all_situations(
    session: AsyncSession = Depends(get_async_session),
):
    all_situations = await read_all_situations_with_tags_from_db(session)
    return all_situations


@router.post(
    "/situation",
    response_model=SituationDB,
    response_model_exclude_none=True,
)
async def create_new_meeting_room(
    situation: Situation,
    session: AsyncSession = Depends(get_async_session),
):
    situation_id = await get_situation_id_by_name(situation.title, session)
    if situation_id is not None:
        raise HTTPException(
            status_code=422,
            detail="Ситуация с таким названием уже существует!",
        )
    new_situation = await create_situation(situation, session)
    return new_situation
