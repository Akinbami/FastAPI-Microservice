from fastapi import FastAPI
from app.api.cast import casts
from app.api.db import create_db_and_tables

app = FastAPI(openapi_url="/api/v1/casts/openapi.json",
              docs_url="/api/v1/casts/docs")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(casts, prefix='/api/v1/casts', tags=['casts'])
