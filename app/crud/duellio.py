# app/crud/duellio.py

from typing import Optional, Union

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.crud.base import CRUDBase
from app.crud.tags import tags_crud
from app.models.duellio import Situation, Tags, situation_tags


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
                tag = await tags_crud.get_or_create_tag_by_name(
                    tag_name, session
                )
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

    async def read_all_situations_with_tags_from_db_by_attribute(
        self,
        attr_name: str,
        attr_value: str,
        session: AsyncSession,
    ):
        attr = getattr(self.model, attr_name)
        db_situations = await session.execute(
            select(Situation)
            .where(attr == attr_value)
            .options(joinedload(Situation.tags))
        )
        return db_situations.scalars().unique().all()

    async def read_situation_with_tags_from_db_by_name(
        self,
        situation_title: str,
        session: AsyncSession,
    ):
        db_situation = await session.execute(
            select(Situation)
            .options(joinedload(Situation.tags))
            .where(Situation.title == situation_title)
        )
        return db_situation.scalars().first()

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

    async def update_situation_tags(
        self,
        situation: Situation,
        tags_names: Optional[list[Tags]],
        clear: bool,
        session: AsyncSession,
    ) -> Optional[Situation]:
        db_situation = await self.read_situation_with_tags_from_db_by_name(
            situation.title, session
        )
        if db_situation is None:
            return None
        if clear:
            db_situation.tags.clear()
        for tag_name in tags_names:
            tag = await tags_crud.get_or_create_tag_by_name(tag_name, session)
            db_situation.tags.append(tag)
        await session.commit()
        await session.refresh(db_situation)
        return db_situation

    async def get_situations_by_tags(
        self,
        tags: list[Tags],
        session: AsyncSession,
    ) -> list[Situation]:
        tags_names = [tag.name for tag in tags]
        subquery = await session.execute(
            select(situation_tags).join(Tags).where(Tags.name.in_(tags_names))
        )
        situation_ids = subquery.scalars().unique().all()
        db_situations = await session.execute(
            select(Situation)
            .options(joinedload(Situation.tags, innerjoin=True))
            .where(Situation.id.in_(situation_ids))
        )
        return db_situations.scalars().unique().all()

    async def get_situations_by_keywords(
        self, keywords: list[str], session: AsyncSession
    ) -> list[Situation]:
        """
        Поиск ситуаций по ключевым словам
        """
        conditions = []
        for search_string in keywords:
            conditions.append(Situation.text.ilike(f"%{search_string}%"))

        db_situations = await session.execute(
            select(Situation)
            .options(joinedload(Situation.tags, innerjoin=True))
            .where(or_(*conditions))
        )
        return db_situations.scalars().unique().all()


duellio_crud = CRUDDuellio(Situation)
