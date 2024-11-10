from fastapi import APIRouter, Header, HTTPException, Depends, Query
from app.api.models import Movie, MovieCreate, MoviePublic, MovieUpdate
from app.api.db import get_session
from typing import List, Annotated
from sqlmodel import Session, select
from app.api.service import is_cast_present

movies = APIRouter()

SessionDep = Annotated[Session, Depends(get_session)]


@movies.post("/", status_code=201)
async def create_movie(movie: MovieCreate, session: SessionDep):
    for cast_id in movie.cast:
        if not is_cast_present(cast_id):
            raise HTTPException(
                status_code=404, detail=f"Cast with id:{cast_id} not found")

    db_movie = Movie.model_validate(movie)
    session.add(db_movie)
    session.commit()
    session.refresh(db_movie)
    return db_movie


@movies.get("/")
async def list_movies(session: SessionDep,
                      offset: int = 0,
                      limit: Annotated[int, Query(le=100)] = 100
                      ) -> List[MoviePublic]:
    movies = session.exec(select(Movie).offset(offset).limit(limit)).all()
    return movies


@movies.get("/{movie_id}")
def read_movie(movie_id: int, session: SessionDep) -> MoviePublic:
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Hero not found")
    return movie


@movies.put("/{movie_id}")
async def update_movie(movie_id: int, dto: MovieUpdate, session: SessionDep):
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    movie_data = dto.model_dump(exclude_unset=True)
    movie.sqlmodel_update(movie_data)

    session.add(movie)
    session.commit()
    session.refresh()

    return movie


@movies.delete('/{movie_id}')
async def delete_movie(movie_id: int, session: SessionDep):
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    session.delete(movie)
    session.commit()
    return {"ok": True}
