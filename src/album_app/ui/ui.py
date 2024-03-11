import os
from datetime import date

import folium
import pandas as pd
import requests
import streamlit as st
from streamlit_folium import st_folium

st.set_page_config(
    page_title="MemGlobe",
    page_icon="🌍",
)

# TODO: Add authentication method
status_auth = True

if "country" not in st.session_state:
    st.session_state["country"] = "France"
if "file_uploader_key" not in st.session_state:
    st.session_state["file_uploader_key"] = 0


@st.cache_data
def get_photos():
    # TODO: Replace with API call
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


def get_locations(locations: pd.DataFrame):
    cols_location = st.columns(2)
    with cols_location[0]:
        country = st.selectbox(
            "Country",
            key="country",
            options=locations["country"].sort_values().unique(),
        )
    with cols_location[1]:
        city = st.selectbox(
            "City",
            key="city",
            options=locations[locations["country"] == country]["city"].unique(),
        )
    return country, city


def clear_form():
    st.session_state["name"] = ""
    st.session_state["date_taken"] = date.today()
    st.session_state["country"] = "France"
    st.session_state["city"] = "Paris"
    st.session_state["file_uploader_key"] += 1


def map():
    default_location = [48.856614, 2.348803]  # Paris, France (example)
    map = folium.Map(location=default_location, zoom_start=5)

    return map


def main():
    if status_auth:
        st.title("MemGlobe 🌍")
        st.write("Welcome to MemGlobe! Your photos all around the world! :sunglasses:")

        # Retrieve data
        photos = get_photos()
        locations = pd.read_csv(
            os.path.join(os.path.dirname(__file__), "data", "worldcities.csv")
        )

        add_photo_expander = st.expander("Add photo")
        with add_photo_expander:
            add_photo_container = st.container(border=True)
            with add_photo_container:
                name = st.text_input("Photo Name", key="name")
                date_taken = st.date_input(
                    "Date Taken",
                    format="YYYY-MM-DD",
                    key="date_taken",
                )
                country, city = get_locations(locations)

                image_file = st.file_uploader(
                    "Upload Image (limit 5 MB)",
                    type=["jpg", "jpeg", "png"],
                    accept_multiple_files=False,
                    key=st.session_state["file_uploader_key"],
                )
                # Check for file size and disable button if needed
                is_file_valid = True
                if image_file:
                    if image_file.size > 5 * 1024 * 1024:  # 5 MB limit
                        st.error(
                            "Image file size exceeds 5 MB limit. Please choose a smaller file."
                        )
                        is_file_valid = False

                # Disable button until all fields are filled
                is_all_filled = all(
                    [
                        name,
                        date_taken,
                        country,
                        city,
                        image_file,
                        is_file_valid,
                    ]
                )
                submit_button = st.button(
                    "Add Photo",
                    disabled=not is_all_filled,
                    on_click=clear_form,
                )

                if submit_button:
                    # TODO: Add API call
                    photos.append(
                        {
                            "id": len(photos) + 1,
                            "name": name,
                            "date_taken": date_taken,
                            "location": f"{country}, {city}",
                            "data": image_file,
                            "album_id": 1,
                        }
                    )
                    st.success("Photo added successfully!")
                    photos = get_photos()

        # Show photos and map
        st.write(photos)
        m = map()
        st_map = st_folium(m, width=700, height=500)


if __name__ == "__main__":
    main()
