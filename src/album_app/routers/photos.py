from album_app.database import crud, schemas
from album_app.database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/photos",
    tags=["photos"],
)


@router.get("/", response_model=list[schemas.Photo])
async def read_photos(db: Session = Depends(get_db)):
    return crud.get_photos(db, skip=0, limit=100)


@router.get("/{photo_id}", response_model=schemas.Photo)
async def read_photo(photo_id: int, db: Session = Depends(get_db)):
    photo = crud.get_photo(db, photo_id)
    if not photo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found"
        )
    return photo


@router.post("/", response_model=schemas.Photo)
async def add_photo(request: schemas.PhotoCreate, db: Session = Depends(get_db)):
    return crud.create_photo(db, request)


@router.delete("/{photo_id}")
async def delete_photo(photo_id: int, db: Session = Depends(get_db)):
    photo = crud.delete_photo(db, photo_id)
    if not photo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found"
        )
    return {"status": "success", "message": "Photo deleted successfully!"}


@router.delete("/")
async def delete_photos(db: Session = Depends(get_db)):
    return crud.delete_photos(db)
