import pandas as pd
import pydeck as pdk
import streamlit as st

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="GDP Visualization", page_icon=":chart_with_upwards_trend:")

def load_data():
    # Simulate loading simple data
    # Assume data format: latitude, longitude, GDP, community_name
    data = pd.DataFrame({
        'lat': [34.05, 36.12, 37.77, 34.00],
        'lon': [-118.24, -115.17, -122.42, -118.25],
        'GDP': [10000, 20000, 30000, 40000],  # Simulated GDP values
        'community_name': ['Community A', 'Community B', 'Community C', 'Community D']
    })
    return data

def render_map(data):
    # Define tooltip for displaying data on hover
    tooltip = {
        "html": "<b>Community:</b> {community_name}<br><b>GDP:</b> {GDP}",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    }

    # Create a HexagonLayer
    layer = pdk.Layer(
        "HexagonLayer",
        data,
        get_position='[lon, lat]',
        get_elevation='GDP',
        elevation_scale=50,  # Adjust scale to visually represent GDP appropriately
        radius=50,  # Adjust radius to fit your geographic needs
        extruded=True,
        pickable=True,
        elevation_range=[0, 30000],  # Adjust based on your max GDP
        tooltip=tooltip
    )

    # Define the initial view state
    view_state = pdk.ViewState(
        latitude=data['lat'].mean(),
        longitude=data['lon'].mean(),
        zoom=5,
        pitch=50
    )

    # Create the deck.gl map
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=view_state,
        layers=[layer]
    ))

# Main
data = load_data()
st.title("Interactive GDP Visualization")
render_map(data)
