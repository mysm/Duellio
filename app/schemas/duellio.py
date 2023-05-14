# app/schemas/duellio.py

from typing import List
from pydantic import BaseModel


class Situation(BaseModel):
    title: str
    text: str

    class Config:
        orm_mode = True


class Tags(BaseModel):
    name: str

    class Config:
        orm_mode = True


class SituationSchema(Situation):
    tags: List[Tags]


class TagSchema(Tags):
    situations: List[Situation]