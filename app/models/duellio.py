# app/models/duellio.py
from typing import List

from sqlalchemy import Column, String, Table, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.core.db import Base


situation_tags = Table(
    "situation_tags",
    Base.metadata,
    Column("situation_id", ForeignKey("situation.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class Situation(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    title = Column(String(250), unique=True, nullable=False)
    text = Column(Text, nullable=False)
    standard = Column(Boolean, default=True)
    tags = relationship(
        "Tags", secondary="situation_tags", back_populates="situations"
    )


class Tags(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name = Column(String(250), unique=True, nullable=False)
    situations: Mapped[List[Situation]] = relationship(
        "Situation", secondary="situation_tags", back_populates="tags"
    )
