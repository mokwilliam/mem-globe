from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class PhotoBase(BaseModel):
    name: str
    date_taken: date
    location: str
    data: bytes
    album_id: int


class PhotoCreate(PhotoBase):
    pass


class Photo(PhotoBase):
    id: int

    class Config:
        orm_mode = True


class AlbumBase(BaseModel):
    name: str
    description: Optional[str] = None
    photos: List[Photo] = []


class AlbumCreate(AlbumBase):
    pass


class Album(AlbumBase):
    id: int

    class Config:
        orm_mode = True
