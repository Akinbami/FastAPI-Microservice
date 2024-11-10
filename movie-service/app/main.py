from fastapi import FastAPI
from app.api.movie import movies
from app.api.db import create_db_and_tables

app = FastAPI(openapi_url="/api/v1/movies/openapi.json",
              docs_url="/api/v1/movies/docs")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(movies, prefix='/api/v1/movies', tags=['movies'])
