# app\api\endpoints\tags.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.duellio import duellio_crud, tags_crud
from app.schemas.duellio import Situation, Tags, SituationDB, TagsDB
from app.services.guess_by_context import guess_similar_words

router = APIRouter()


@router.get(
    "/",
    response_model=list[TagsDB],
    response_model_exclude_none=True,
)
async def get_tags(session: AsyncSession = Depends(get_async_session),):
    db_tags = await tags_crud.get_multi(session)
    return db_tags

@router.post(
    "/similar_words"
)
async def get_similar_words(
    word: str,
    topn: int = 5,
    session: AsyncSession = Depends(get_async_session),
):
    similar_words = await guess_similar_words(word, topn)
    return similar_words

@router.post(
    "/",
    response_model=SituationDB,
    response_model_exclude_none=True,
)
async def update_situation_tags(
    situation: Situation,
    tags: list[Tags],
    clear: bool,
    session: AsyncSession = Depends(get_async_session),
):
    situation_id = await duellio_crud.get_situation_id_by_name(
        situation.title, session
    )
    if situation_id is None:
        raise HTTPException(
            status_code=422,
            detail="Ситуации с таким названием не существует!",
        )
    updated_situation = await duellio_crud.update_situation_tags(
        situation, tags, clear, session
    )
    return updated_situation
