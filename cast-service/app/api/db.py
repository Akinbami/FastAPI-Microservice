from sqlmodel import Session, create_engine, SQLModel
from typing import Annotated
import os
from fastapi import Depends

DATABASE_URI = os.environ.get("DATABASE_URI")

engine = create_engine(DATABASE_URI)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
