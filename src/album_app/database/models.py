from datetime import date

from sqlalchemy import BLOB, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    photos = relationship("Photo", back_populates="album")


class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    date_taken = Column(Date, default=date.today(), nullable=False)
    location = Column(String, nullable=False)
    data = Column(BLOB, nullable=False)
    album_id = Column(Integer, ForeignKey("albums.id"))

    album = relationship("Album", back_populates="photos")
