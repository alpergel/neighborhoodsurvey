import pandas as pd
import pydeck as pdk
import streamlit as st

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="GDP Visualization", page_icon=":chart_with_upwards_trend:")

def load_data():
    # Simulate loading simple data
    # Assume data format: latitude, longitude, GDP, community_name
    data = pd.DataFrame({
        'lat': [33, 36.12, 37.77, 34.00],  # Check these coordinates
        'lon': [-117, -115.17, -122.42, -118.25],  # Check these coordinates
        'GDP': [10000, 20000, 30000, 40000],  # Simulated GDP values
        'community_name': ['Community A', 'Community B', 'Community C', 'Community D']
    })
    return data

def render_map(data):
    tooltip = {
        "html": "<b>Community:</b> {community_name}<br><b>GDP:</b> {GDP}",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    }

    layer = pdk.Layer(
        "ColumnLayer",
        data,
        get_position="[lon, lat]",
        get_elevation="GDP",
        elevation_scale=100,  # Adjusted for visibility
        radius=2000,  # Visible radius
        extruded=True,
        pickable=True,
        tooltip=tooltip
    )

    # Setup the initial view state for the map
    view_state = pdk.ViewState(
        latitude=data['lat'].mean(),
        longitude=data['lon'].mean(),
        zoom=5,
        pitch=50
    )

    # Create the deck
    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style='mapbox://styles/mapbox/light-v9'
    ))

st.title("Interactive GDP Visualization")
# Main
data = load_data()
st.write(data.head())
render_map(data)
