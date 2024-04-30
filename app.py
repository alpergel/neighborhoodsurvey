
# Streamlined version of the Streamlit app code

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
    return data

# Function to display the map with corrected tooltip
def map(data, lat, lon, zoom):
    # Since tooltips might not accept columns with spaces or special characters directly,
    # we need to create a copy of the column with a name that's valid as a JavaScript identifier.
    data_copy = data.copy()
    data_copy['census_tract'] = data_copy['Census Tract #']
    
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
                    data=data_copy,
                    get_position=["Lon", "Lat"],
                    get_elevation="Number",
                    elevation_scale=2,
                    elevation_range=[0, 200000],
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
