# app/api/duellio.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page, paginate

from app.core.db import get_async_session
from app.crud.duellio import duellio_crud
from app.schemas.duellio import Situation, SituationDB, SituationSchemaDB, Tags

router = APIRouter()


@router.get(
    "/situation",
    response_model=Page[list[SituationSchemaDB]],
    response_model_exclude_none=True,
)
async def get_all_situations(
    session: AsyncSession = Depends(get_async_session),
):
    all_situations = await duellio_crud.read_all_situations_with_tags_from_db(session)
    return paginate(all_situations)


@router.post(
    "/situation",
    response_model=SituationDB,
    response_model_exclude_none=True,
)
async def create_new_situation(
    situation: Situation,
    tags : list[Tags],
    session: AsyncSession = Depends(get_async_session),
):
    situation_id = await duellio_crud.get_situation_id_by_name(situation.title, session)
    if situation_id is not None:
        raise HTTPException(
            status_code=422,
            detail="Ситуация с таким названием уже существует!",
        )
    new_situation = await duellio_crud.create_situation(situation, tags, session)
    return new_situation
