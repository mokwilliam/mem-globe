from sqlalchemy.orm import Session

from . import models, schemas


def get_photos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Photo).offset(skip).limit(limit).all()


def get_photo(db: Session, photo_id: int):
    return db.query(models.Photo).filter(models.Photo.id == photo_id).first()


def create_photo(db: Session, photo: schemas.PhotoCreate):
    db_photo = models.Photo(**photo.dict())
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return db_photo


def delete_photo(db: Session, photo_id: int) -> bool:
    photo = get_photo(db, photo_id)
    if photo:
        db.delete(photo)
        db.commit()
        return True
    return False


def delete_photos(db: Session) -> bool:
    db.query(models.Photo).delete()
    db.commit()
    return True
