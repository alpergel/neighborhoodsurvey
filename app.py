import pandas as pd
import pydeck as pdk
import streamlit as st

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="GDP Visualization", page_icon=":chart_with_upwards_trend:")

def load_data():
    # Simulate loading simple data
    # Assume data format: latitude, longitude, GDP, community_name
    ipcData = pd.DataFrame({
        'lat': [33.36607, 33.370236, 33.369961, 33.354334],  # Check these coordinates
        'lon': [-111.96315, -111.971805, -111.953024, -111.95699],  # Check these coordinates
        'ipc': [26814, 55927, 40759, 37540],  # Simulated GDP values
        'community_name': ['Community A', 'Community B', 'Community C', 'Community D']
    })
    arcData = pd.DataFrame({
        'lng_h': [-109.9304, -109.9304, -109.9304, -109.9304],
        'lng_w': [-111.96315, -110.911789, -116.375015, -116.3903],
        "lat_h": [27.4828, 27.4828, 27.4828, 27.4828],
        "lat_w": [33.36607, 32.253460,33.255871, 33.8200],
        "com": ["Guadalupe, AZ","Tuscon, AZ","Thousand Palms, CA", "Borrego Springs, CA"]
    })
    return ipcData, arcData
def render_migration_map(data):
    tooltip = {
        "html": "<b>Yaqui Migration To:</b> {com}<br><b>",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    }
    BLUE_RGB = [0, 0, 255, 100]
    RED_RGB = [240, 50, 0, 100]
    arc_layer = pdk.Layer(
        "ArcLayer",
        data=data,
        widthScale=7,
        get_width="S000 * 2",
        get_source_position=["lng_h", "lat_h"],
        get_target_position=["lng_w", "lat_w"],
        get_tilt=15,
        get_source_color=BLUE_RGB,
        get_target_color=RED_RGB,
        pickable=True,
        auto_highlight=True,
    ) 
    meanLat = (data['lat_h'].mean()+data['lat_w'].mean())//2
    meanLon = (data['lng_h'].mean()+data['lng_w'].mean())//2
    view_state = pdk.ViewState(
        latitude=meanLat,
        longitude=meanLon,
        bearing=45,
        pitch=50,
        zoom=8,
    )


    # Create the deck
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v9",
        layers=[arc_layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        
        
    ))

def render_ipc_map(data):
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
ipcData, arcData = load_data()
render_migration_map(arcData)
row1_1, row1_2, row1_3 = st.columns(3)
with row1_1:
    st.title("Local Income Per Capita Comparison")
    render_ipc_map(ipcData)
with row1_2:
    st.title("Local Income Per Capita Comparison")
    render_ipc_map(ipcData)
with row1_3:
    st.title("Local Income Per Capita Comparison")
    render_ipc_map(ipcData)


