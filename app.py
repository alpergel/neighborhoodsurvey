import pandas as pd
import pydeck as pdk
import streamlit as st

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="Data Visualization", page_icon=":chart_with_upwards_trend:")

# Function to load data and correct the column names
def load_data():
    path = "ipc1.csv"  # The path will be adjusted to the actual file location when deploying
    data = pd.read_csv(
        path,
        skiprows=1,  # Skipping the first row assuming it's the header
        names=["lat", "lon", "num", "tract"],
    )
    return data

# Function to display the map with corrected tooltip
def map(data, lat, lon, zoom):
    tooltip = {
        "html": "<b>Census Tract #:</b> {tract}<br><b>Number:</b> {num}",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    }
    layer = pdk.Layer(
        'HexagonLayer',
        data,
        get_position='[lon, lat]',
        auto_highlight=True,
        get_elevation="num",
        elevation_scale=50,
        pickable=True,
        elevation_range=[0, 3000],
        extruded=True,
        coverage=1,
        radius=250,  # Adjusted for smaller hexagons; previously not defined, so it was using the default size
    )
    
    st.write(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state={"latitude": lat, "longitude": lon, "zoom": zoom, "pitch": 50},
            layers=[layer],
            tooltip=tooltip,
        )
    )

# Main app execution part
data = load_data()
midpoint = (data['lat'].mean(), data['lon'].mean())

st.title("Interactive Data Visualization")
map(data, midpoint[0], midpoint[1], 11)