# app/crud/duellio.py

from typing import Optional, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.crud.base import CRUDBase
from app.crud.tags import tags_crud
from app.models.duellio import Situation, Tags


class CRUDDuellio(CRUDBase):
    async def create_situation(
        self,
        new_situation: Situation,
        tags_names: Optional[list[Tags]],
        session: AsyncSession,
    ) -> Situation:
        new_situation_data = new_situation.dict()
        db_situation = Situation(**new_situation_data)
        if tags_names:
            for tag_name in tags_names:
                tag = await tags_crud.get_or_create_tag_by_name(tag_name, session)
                db_situation.tags.append(tag)
        session.add(db_situation)
        await session.commit()
        await session.refresh(db_situation)
        return db_situation

    async def read_all_situations_from_db(
        self,
        session: AsyncSession,
    ) -> list[Situation]:
        db_situations = await self.get_multi(session)
        return db_situations

    async def read_all_situations_with_tags_from_db(
        self,
        session: AsyncSession,
    ):
        db_situations = await session.execute(
            select(Situation).options(joinedload(Situation.tags))
        )
        return db_situations.scalars().unique().all()

    async def get_situation_by_id(
        self,
        situation_id: int,
        session: AsyncSession,
    ) -> Union[Situation, None]:
        db_situation = await self.get(situation_id, session)
        return db_situation

    async def get_situation_id_by_name(
        self,
        situation_title: str,
        session: AsyncSession,
    ) -> Optional[int]:
        db_situation = await self.get_by_attribute(
            "title", situation_title, session
        )
        result = None
        if db_situation is not None:
            result = db_situation.id
        return result


duellio_crud = CRUDDuellio(Situation)

