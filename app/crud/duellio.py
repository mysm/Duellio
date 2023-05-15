# app/crud/duellio.py

from typing import Optional, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.duellio import Situation, Tags


async def create_situation(
    new_situation: Situation, session: AsyncSession
) -> Situation:
    new_situation_data = new_situation.dict()
    db_situation = Situation(**new_situation_data)
    session.add(db_situation)
    await session.commit()
    await session.refresh(db_situation)
    return db_situation


async def read_all_situations_from_db(
    session: AsyncSession,
) -> list[Situation]:
    db_situations = await session.execute(select(Situation))
    return db_situations.scalars().all()


async def read_all_situations_with_tags_from_db(
    session: AsyncSession,
):
    db_situations = await session.execute(select(Situation).options(joinedload(Situation.tags)))
    return db_situations.scalars().unique().all()



async def get_situation_by_id(
    situation_id: int,
    session: AsyncSession,
) -> Union[Situation, None]:
    db_situation = await session.execute(
        select(Situation).where(Situation.id == situation_id)
    )
    db_situation = db_situation.scalars().first()
    return db_situation


async def get_situation_id_by_name(
    situation_title: str,
    session: AsyncSession,
) -> Optional[int]:
    db_situation_id = await session.execute(
        select(Situation.id).where(Situation.title == situation_title)
    )
    db_situation_id = db_situation_id.scalars().first()
    return db_situation_id
