import uvicorn
from album_app.routers import photos
from fastapi import FastAPI

app = FastAPI()

app.include_router(photos.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
