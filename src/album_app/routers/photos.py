from fastapi import APIRouter

router = APIRouter(
    prefix="/photos",
    tags=["photos"],
)


@router.get("/")
async def read_photos():
    return [
        {"photo_id": "1", "photo_name": "photo1"},
        {"photo_id": "2", "photo_name": "photo2"},
    ]


@router.get("/{photo_id}")
async def read_photo(photo_id: int):
    return {"photo_id": photo_id, "photo_name": f"photo{photo_id}"}


@router.post("/")
async def add_photo(photo_id: int, photo_name: str):
    return {"photo_id": photo_id, "photo_name": photo_name}
