from typing import Union, Optional
from sqlmodel import SQLModel, Field


class CastBase(SQLModel):
    name: str = Field(default=None, index=True)
    nationality: Union[str, None] = Field(default=None)


class Cast(SQLModel, table=True):
    id: int = Field(primary_key=True)


class CastPublic(CastBase):
    id: int


class CastUpdate(CastBase):
    name: Union[str, None] = None
    nationality: Union[str, None] = None
