# app/models/duellio.py

# Добавьте импорт класса Text.
from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from app.core.db import Base


class Situation(Base):
    title = Column(String(250), unique=True, nullable=False)
    text = Column(Text, nullable=False)
    tags = relationship("Situation", secondary="situations_tags", back_populates="situations")


class Tags(Base):
    name = Column(String(250), unique=True, nullable=False)
    situations = relationship("Tag", secondary="situations_tags", back_populates="tags")


