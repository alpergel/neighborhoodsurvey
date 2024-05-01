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
        'ipc': [26814, 55927, 40759, 37540],  # Simulated GDP values
        'community_name': ['Community A', 'Community B', 'Community C', 'Community D']
    })
    return data

def render_map(data):
    tooltip = {
        "html": "<b>Census Tract:</b> {community_name}<br><b>Income Per Capita:</b> {ipc}",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    }
        
    layer = pdk.Layer(
        "ColumnLayer",
        data,
        get_position="[lon, lat]",
        get_elevation="ipc",
        auto_highlight=True,
        get_fill_color=[108, 166, 86 ],  
        elevation_scale=0.05,  # Adjusted for visibility
        radius=200,  # Visible radius
        extruded=True,
        pickable=True,
        
    )

    # Setup the initial view state for the map
    view_state = pdk.ViewState(
        latitude=data['lat'].mean(),
        longitude=data['lon'].mean(),
        zoom=10,
        pitch=50
    )

    # Create the deck
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v9",
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        
        
    ))
st.title("Guadalupe: A Rooted City of Hope and Migration")
data = load_data()
row1_1, row1_2, row1_2 = st.columns(3)
with row1_1:
    st.title("Local Income Per Capita Comparison")
    render_map(data)
with row1_2:
    st.title("Local Income Per Capita Comparison")
    render_map(data)
with row1_3:
    st.title("Local Income Per Capita Comparison")
    render_map(data)


