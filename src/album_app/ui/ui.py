import base64
import os
from datetime import date
from io import BytesIO

import folium
import pandas as pd
import requests
import streamlit as st
from album_app.ui.auth.authenticate import get_authenticator
from PIL import Image
from streamlit_folium import st_folium

st.set_page_config(
    page_title="MemGlobe",
    page_icon="🌍",
    layout="wide",
)

### LOGIN TEST ###
# username: bshelton
# password: abc
#
# username: cwoods
# password: def


def init_session_state():
    if "current_country" not in st.session_state:
        st.session_state["current_country"] = "France"
    if "file_uploader_key" not in st.session_state:
        st.session_state["file_uploader_key"] = 0
    if "photos" not in st.session_state:
        st.session_state["photos"] = get_photos()


def clear_form(name, date_taken, country, city, encoded_image):
    photo = requests.post(
        "http://127.0.0.1:8000/photos",
        json={
            "name": name,
            "date_taken": date_taken.strftime("%Y-%m-%d"),
            "location": f"{country}, {city}",
            "data": encoded_image,
        },
    )
    st.session_state["photos"].append(photo.json())
    st.session_state["photo_name"] = ""
    st.session_state["date_taken"] = date.today()
    st.session_state["current_country"] = "France"
    st.session_state["current_city"] = "Paris"
    st.session_state["file_uploader_key"] += 1


@st.cache_data
def get_photos():
    photos = requests.get("http://127.0.0.1:8000/photos").json()
    return photos


def show_photos():
    cols = st.columns(3)
    for i, photo in enumerate(st.session_state["photos"]):
        with cols[i % 3]:
            # Convert base64 (BLOB) to image
            decoded_bytes = base64.b64decode(photo["data"])
            image = Image.open(BytesIO(decoded_bytes))
            st.image(
                image,
                caption=f"{photo['name']} • {photo['date_taken']} • {photo['location']}",
                use_column_width=True,
            )


def get_locations(locations: pd.DataFrame):
    cols_location = st.columns(2)
    with cols_location[0]:
        country = st.selectbox(
            "Country",
            key="current_country",
            options=locations["country"].sort_values().unique(),
        )
    with cols_location[1]:
        city = st.selectbox(
            "City",
            key="current_city",
            options=locations[locations["country"] == country]["city"].unique(),
        )
    return country, city


def form(locations: pd.DataFrame):
    add_photo_expander = st.expander("Add photo")
    with add_photo_expander:
        add_photo_container = st.container(border=True)
        with add_photo_container:
            col_name, col_date = st.columns(2)
            with col_name:
                name = st.text_input("Photo Name", max_chars=50, key="photo_name")
            with col_date:
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
            encoded_image = ""
            if image_file:
                if image_file.size > 5 * 1024 * 1024:  # 5 MB limit
                    st.error(
                        "Image file size exceeds 5 MB limit. Please choose a smaller file."
                    )
                    is_file_valid = False
                else:
                    st.image(image_file, width=75)
                    # Convert image to BLOB
                    encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

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
                args=(name, date_taken, country, city, encoded_image),
            )

            if submit_button:
                st.success("Photo added successfully!")
                st.cache_data.clear()


def init_map(locations: pd.DataFrame):
    map = folium.Map(
        location=[48.856614, 2.348803],
        zoom_start=5,
    )
    fg = folium.FeatureGroup(name="Photos")
    marker_cluster = folium.plugins.MarkerCluster().add_to(fg)
    marker_cluster_loc = {}

    # Count number of photos per location
    for photo in st.session_state["photos"]:
        location = photo["location"]
        if location not in marker_cluster_loc:
            marker_cluster_loc[location] = 1
        else:
            marker_cluster_loc[location] += 1

    # Add markers
    for loc, nb_photo in marker_cluster_loc.items():
        country, city = loc.split(", ")
        marker = folium.Marker(
            location=locations[
                (locations["country"] == country) & (locations["city"] == city)
            ][["lat", "lng"]].values[0],
            popup=f"Nb photos: {nb_photo}",
            icon=folium.Icon(color="blue", icon="camera"),
        )
        marker_cluster.add_child(marker)

    st.session_state["map"] = map
    st.session_state["feature_group"] = fg


def main():
    authenticator = get_authenticator()
    name, _, _ = authenticator.login()
    if st.session_state["authentication_status"] is False:
        st.error("Username/password is incorrect")
    elif st.session_state["authentication_status"] is None:
        st.warning("Please enter your username and password")
    else:
        init_session_state()
        st.title("MemGlobe 🌍")
        st.subheader(
            "Welcome to MemGlobe! Your photos all around the world! :sunglasses:"
        )
        st.caption(f"*Connected as {name}*")
        authenticator.logout()

        # Retrieve data
        locations = pd.read_csv(
            os.path.join(os.path.dirname(__file__), "data", "worldcities.csv")
        )

        col1, col2 = st.columns(2)
        with col1:
            # Form + photos
            form(locations)
            show_photos()

        with col2:
            # Init map
            init_map(locations)

            # Show map
            st_folium(
                st.session_state["map"],
                feature_group_to_add=st.session_state["feature_group"],
                width=800,
                height=600,
            )


if __name__ == "__main__":
    main()
