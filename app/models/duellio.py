# app/models/duellio.py

# Добавьте импорт класса Text.
from sqlalchemy import Column, String, Text, Table, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.core.db import Base

situation_tags = Table(
    "situation_tags",
    Base.metadata,
    Column("situation_id", ForeignKey("situation.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class Situation(Base):
    title = Column(String(250), unique=True, nullable=False)
    text = Column(Text, nullable=False)
    standard = Column(Boolean, default=True)
    tags = relationship(
        "Tags", secondary="situation_tags", back_populates="situations"
    )


class Tags(Base):
    name = Column(String(250), unique=True, nullable=False)
    situations = relationship(
        "Situation", secondary="situation_tags", back_populates="tags"
    )
