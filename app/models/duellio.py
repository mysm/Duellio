# app/models/duellio.py

# Добавьте импорт класса Text.
from sqlalchemy import Column, String, Text, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db import Base

situation_tags = Table(
    "situations_tags",
    Base.metadata,
    Column("situation_id", ForeignKey("situation.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class Situation(Base):
    title = Column(String(250), unique=True, nullable=False)
    text = Column(Text, nullable=False)
    tags = relationship(
        "Situation", secondary="situation_tags", back_populates="situations"
    )


class Tags(Base):
    name = Column(String(250), unique=True, nullable=False)
    situations = relationship(
        "Tag", secondary="situation_tags", back_populates="tags"
    )
