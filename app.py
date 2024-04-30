
# Streamlined version of the Streamlit app code with corrected column names and tooltips

import pandas as pd
import pydeck as pdk
import streamlit as st

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="Data Visualization", page_icon=":chart_with_upwards_trend:")

# Function to load data and correct the column names
def load_data():
    path = "ips.csv"  # The path will be adjusted to the actual file location when deploying
    data = pd.read_csv(
        path,
        skiprows=1  # Skipping the first row assuming it's the header
    )
    # Renaming the columns to match the expected format for Pydeck
    data = data.rename(columns=lambda x: x.strip().replace(' ', '_').replace('#', 'num').capitalize())
    return data

# Function to display the map with corrected tooltip
def map(data, lat, lon, zoom):
    tooltip = {
        "html": "<b>Census Tract #:</b> {Census_tract_num}<br><b>Number:</b> {Number}",
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
