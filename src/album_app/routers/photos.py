from fastapi import APIRouter

router = APIRouter(
    prefix="/photos",
    tags=["photos"],
)


@router.get("/")
async def read_photos():
    return [
        {
            "id": 1,
            "name": "photo1",
            "date_taken": "2022-01-01",
            "location": "New York",
            "data": "data1",
            "album_id": 1,
        },
        {
            "id": 2,
            "name": "photo2",
            "date_taken": "2022-01-02",
            "location": "Los Angeles",
            "data": "data2",
            "album_id": 1,
        },
    ]


@router.get("/{photo_id}")
async def read_photo(photo_id: int):
    return {"photo_id": photo_id, "photo_name": f"photo{photo_id}"}


@router.post("/")
async def add_photo(photo_id: int, photo_name: str):
    return {"photo_id": photo_id, "photo_name": photo_name}
