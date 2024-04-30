import pandas as pd
import pydeck as pdk
import streamlit as st

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="GDP Visualization", page_icon=":chart_with_upwards_trend:")

def load_data():
    # Simulate loading simple data
    # Assume data format: latitude, longitude, GDP, community_name
    data = pd.DataFrame({
        'lat': [33.36607, 33.370236, 33.369961, 33.354334],  # Check these coordinates
        'lon': [-111.96315, -111.971805, -111.953024, -111.95699],  # Check these coordinates
        'GDP': [26814, 55927, 40759, 37540],  # Simulated GDP values
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
    
    max_gdp = data['GDP'].max()
    color_scale = [[x / max_gdp * 255, (1 - x / max_gdp) * 255, 100] for x in data['GDP']]
    
    layer = pdk.Layer(
        "ColumnLayer",
        data,
        get_position="[lon, lat]",
        get_elevation="GDP",
        auto_highlight=True,
        get_fill_color=["GDP/10 * 255", "(1 - GDP/10 ) * 255", 100],  # Coloring based on GDP
        elevation_scale=4,  # Adjusted for visibility
        radius=2000,  # Visible radius
        extruded=True,
        pickable=True,
        
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
        map_style="mapbox://styles/mapbox/light-v9",
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        
        
    ))

st.title("Interactive GDP Visualization")
# Main
data = load_data()
st.write(data.head())
render_map(data)
