# MemGlobe

This project focuses on developing a web application for managing a photo album with an interactive map view.

## Help from:

- [Poetry](https://python-poetry.org)
- [FastAPI](https://fastapi.tiangolo.com)
- [SQLAlchemy](https://www.sqlalchemy.org)
- [Pydantic](https://docs.pydantic.dev/latest/)
- [Folium](https://python-visualization.github.io/folium/latest/user_guide.html)
- [Streamlit](https://docs.streamlit.io)
- [Pytest](https://docs.pytest.org)
- Google Gemini

## Overview

In this project, we are creating a web app that offers users the ability to manage a photo album with an interactive map view. The app will allow users to:

- Upload photos with details like name, date taken, location...
- Store photos securely in the database using a Blob (Binary Large Object) format.
- Click on map markers to see detailed information about the corresponding photos.

===> **A GIF WILL BE INSERTED HERE TO SHOW THE APP** <===

## Steps followed

### 0. Installation & Setup

- Poetry project

```bash
pip install poetry

# `poetry init --no-interaction` to initialize a pre-existing project
poetry new src --name="album_app"
cd src
poetry add fastapi sqlalchemy psycopg2 pydantic=1.10.14 uvicorn streamlit folium pytest
pip install python-dotenv # to use .env file
# `poetry shell` to access the environment in the terminal and `exit` to exit the environment
```

- Run the code (without Docker)

```bash
# In the src folder
poetry run uvicorn album_app.main:app --reload

poetry run streamlit run album_app/ui/ui.py
```

### 1. Project architecture

- `src`: contains the Python code
  - `album_app`: contains the code for the API (FastAPI)
    - `database`: contains the code to interact with the database
    - `routers`: contains the code for the routes

### Interesting points / Issues I encountered

- **Folium** is a great library to create interactive maps.
- **Streamlit** is a great library to create web apps with Python.

### Possible improvements

- Make the app work on a Docker container

### Extra: Setup of pytest

Once the test files are written, we can run the tests.

```bash
pip install pytest

# To run tests
pytest
```

### Extra: Setup of pre-commit

```bash
pip install pre-commit
```

Once the `.pre-commit-config.yaml` completed, we need to set up the git hooks scripts.

```bash
pre-commit install
```
