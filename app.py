
# Streamlined version of the Streamlit app code with fixed tooltips

import pandas as pd
import pydeck as pdk
import streamlit as st

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="Data Visualization", page_icon=":chart_with_upwards_trend:")

# Function to load data
def load_data():
    path = "ips.csv"
    data = pd.read_csv(
        path,
        names=["Lat", "Lon", "Number", "Census Tract #"],
        skiprows=1
    )
    # Renaming the column to ensure compatibility with tooltip in Pydeck
    data = data.rename(columns={'Census Tract #': 'census_tract'})
    return data

# Function to display the map with fixed tooltip
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
                    coverage=1,
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
