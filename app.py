
# Streamlined version of the Streamlit app code with corrected tooltips

import pandas as pd
import pydeck as pdk
import streamlit as st

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="Data Visualization", page_icon=":chart_with_upwards_trend:")

# Function to load data
def load_data():
    path = "ips.csv"  # The path will be adjusted to the actual file location when deploying
    data = pd.read_csv(
        path,
        skiprows=1  # Skipping the first row assuming it's the header
    )
    # Renaming the column with special characters to ensure compatibility with Pydeck
    data = data.rename(columns={'Census Tract #': 'census_tract'})
    return data

# Function to display the map with corrected tooltip
def map(data, lat, lon, zoom):
    tooltip = {
        "html": "<b>Census Tract #:</b> {census_tract}<br><b>Number:</b> {Number}",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    }
    
    st.write(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state={"latitude": lat, "longitude": lon, "zoom": zoom, "pitch": 50},
            layers=[
                pdk.Layer(
                    "HexagonLayer",
                    data=data,
                    get_position=["Lon", "Lat"],
                    get_elevation="Number",
                    elevation_scale=4,
                    elevation_range=[0, 1000],
                    pickable=True,
                    extruded=True,
                ),
            ],
            tooltip=tooltip
        )
    )

# Main app execution part
data = load_data()
midpoint = (data['Lat'].mean(), data['Lon'].mean())

st.title("Interactive Data Visualization")
map(data, midpoint[0], midpoint[1], 11)
