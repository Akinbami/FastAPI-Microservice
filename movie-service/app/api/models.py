from pydantic import BaseModel
from typing import List, Union
from sqlmodel import SQLModel, Field, Column, JSON


class MovieBase(SQLModel):
    name: str = Field(index=True)
    plot: str = Field()
    genres: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    casts: List[int] = Field(default_factory=list, sa_column=Column(JSON))


class Movie(MovieBase, table=True):
    id: Union[int, None] = Field(default=None, primary_key=True)
    secret_title: str


class MoviePublic(MovieBase):
    id: int


class MovieCreate(MovieBase):
    secret_title: str


class MovieUpdate(MovieBase):
    name: Union[str, None] = None
    plot: Union[str, None] = None
    genres: Union[List[str], List[None]] = Field(
        default_factory=list, sa_column=Column(JSON))
    casts: Union[List[str], List[None]] = Field(
        default_factory=list, sa_column=Column(JSON))
