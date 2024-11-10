from fastapi import APIRouter, HTTPException, Query
from typing import Annotated
from app.api.models import Cast, CastBase, CastPublic
from app.api.db import SessionDep
from sqlmodel import select

casts = APIRouter()


@casts.post('/')
async def add_cast(cast: CastBase, session: SessionDep) -> Cast:
    db_cast = CastBase.model_validate(cast)
    session.add(db_cast)
    session.commit()
    session.refresh(db_cast)
    return db_cast


@casts.get('/')
async def list_cast(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=10)] = 10):
    casts = session.exec(select(Cast).offset(offset).limit(limit)).all()
    return casts


@casts.get('/{cast_id}')
async def get_cast(cast_id: int, session: SessionDep) -> CastPublic:
    cast = session.get(Cast, cast_id)
    if not cast:
        raise HTTPException(status_code=404, detail="cast not found")
    return cast


# @casts.put('/casts/{cast_id}')
# async def update_cast():
#     pass


# @casts.delete('/casts/{cast_id}')
# async def delete_cast():
#     pass
