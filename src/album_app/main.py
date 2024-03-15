import uvicorn
from album_app.database.database import engine
from album_app.database.models import Base
from album_app.routers import photos
from fastapi import FastAPI

app = FastAPI()

app.include_router(photos.router)


@app.on_event("startup")
async def init_db():
    # Create the database tables if they do not exist
    Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
