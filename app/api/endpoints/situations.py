# app/api/duellio.py
import warnings

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page, paginate, Params
from fastapi_pagination.utils import FastAPIPaginationWarning


from app.core.db import get_async_session
from app.crud.duellio import duellio_crud
from app.schemas.duellio import Situation, SituationDB, SituationSchemaDB, Tags

router = APIRouter()


@router.get(
    "/",
    response_model=Page[SituationSchemaDB],
    response_model_exclude_none=True,
)
async def get_all_situations(
    session: AsyncSession = Depends(get_async_session),
    params: Params = Depends(),
):
    all_situations = await duellio_crud.read_all_situations_with_tags_from_db(
        session
    )
    warnings.simplefilter("ignore", FastAPIPaginationWarning)
    return paginate(all_situations, params)


@router.post(
    "/",
    response_model=SituationDB,
    response_model_exclude_none=True,
)
async def create_new_situation(
    situation: Situation,
    tags: list[Tags],
    session: AsyncSession = Depends(get_async_session),
):
    situation_id = await duellio_crud.get_situation_id_by_name(
        situation.title, session
    )
    if situation_id is not None:
        raise HTTPException(
            status_code=422,
            detail="Ситуация с таким названием уже существует!",
        )
    new_situation = await duellio_crud.create_situation(
        situation, tags, session
    )
    return new_situation
