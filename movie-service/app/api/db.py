from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine
from typing import Annotated
import os

DATABASE_URL = os.getenv('DATABASE_URI')

engine = create_engine(DATABASE_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
