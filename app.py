import pandas as pd
import pydeck as pdk
import streamlit as st
import numpy as np

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="Data Visualization", page_icon=":chart_with_upwards_trend:")

# Function to load data and correct the column names
def load_data():
    path = "ipc2.csv"  # The path will be adjusted to the actual file location when deploying
    data = pd.read_csv(
        path,
        skiprows=1,  # Skipping the first row assuming it's the header
        names=["lat", "lon"],
    )
    
    #replicated_data = data.loc[data.index.repeat(data['num'])].copy()
    #replicated_data.reset_index(drop=True, inplace=True)

    # Optionally, you may want to drop or modify the 'num' column since it has served its purpose
    #replicated_data.drop('num', axis=1, inplace=True)
    #replicated_data.drop('tract', axis=1, inplace=True)

    return data

# Function to display the map with corrected tooltip
def map(data, lat, lon, zoom):
    layer = pdk.Layer(
        'HexagonLayer',
        data,
        get_position='[lon, lat]',
        auto_highlight=True,
        get_elevation="num",
        elevation_scale=10,
        pickable=True,
        elevation_range=[0, 500],
        extruded=True,
        coverage=1,
        radius=250,  # Adjusted for smaller hexagons; previously not defined, so it was using the default size
    )
    
    st.write(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/dark-v9",
            initial_view_state={"latitude": lat, "longitude": lon, "zoom": zoom, "pitch": 50},
            layers=[layer],
        )
    )

# Main app execution part
data = load_data()
midpoint = (data['lat'].mean(), data['lon'].mean())

st.title("Interactive Data Visualization")
st.write(data.head())
map(data, midpoint[0], midpoint[1], 11)