import os

from sqlmodel import create_engine, SQLModel, Session

from dotenv import load_dotenv


if os.path.exists(".env.dev"):
    load_dotenv(".env.dev")

DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session