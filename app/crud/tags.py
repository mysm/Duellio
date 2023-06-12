# app/crud/tags.py

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.duellio import Tags


class CRUDTag(CRUDBase):
    async def get_or_create_tag_by_name(
        self, tag: Tags, session: AsyncSession
    ) -> Tags:
        new_tag = await self.get_by_attribute("name", tag.name, session)
        if new_tag is None:
            new_tag = await self.create(tag, session)
        return new_tag


tags_crud = CRUDTag(Tags)
