import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

PATH_DATABASE = os.path.join(os.path.dirname(__file__), "sql_album_app.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///./{PATH_DATABASE}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
