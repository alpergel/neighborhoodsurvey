import pandas as pd
import pydeck as pdk
import streamlit as st

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="Guadalupe Neighborhood Survey", page_icon=":cactus:")

def load_data():
    # Simulate loading simple data
    # Assume data format: latitude, longitude, GDP, community_name
    ipcData = pd.DataFrame({
        'lat': [33.36607, 33.370236, 33.369961, 33.354334],  # Check these coordinates
        'lon': [-111.96315, -111.971805, -111.953024, -111.95699],  # Check these coordinates
        'ipc': [26814, 55927, 40759, 37540],  # Simulated GDP values
        'census_tract': ['4013320002', '4013116738', '4013320007', '4013320001']
    })
    arcData = pd.DataFrame({
        'lng_h': [-109.9304, -109.9304, -109.9304, -109.9304, -109.9304],
        'lng_w': [-111.96315, -110.911789, -116.375015, -116.3903, -101.855072],
        "lat_h": [27.4828, 27.4828, 27.4828, 27.4828, 27.4828],
        "lat_w": [33.36607, 32.253460,33.255871, 33.8200, 33.576698],
        "com": ["Guadalupe, AZ","Tuscon, AZ","Thousand Palms, CA", "Borrego Springs, CA", "Lubbock, TX"]
    })
    mobilityData = pd.DataFrame({
        'lat': [33.36607, 33.370236, 33.369961, 33.354334],
        'lon': [-111.96315, -111.971805, -111.953024, -111.95699],
        'mob': [2,6,9,6],
        'census_tract': ['4013320002', '4013116738', '4013320007', '4013320001'],
    })
    eduData = pd.DataFrame({
        'lat': [33.36607, 33.370236, 33.369961, 33.354334],
        'lon': [-111.96315, -111.971805, -111.953024, -111.95699],
        'edu': [61,82,100,100],
        'census_tract': ['4013320002', '4013116738', '4013320007', '4013320001'],
    })
    return ipcData, arcData, mobilityData, eduData
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
        zoom=5,
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
        "html": "<b>Census Tract #:</b> {census_tract}<br><b>Income Per Capita:</b> {ipc}",
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
def render_mob_map(data):
    tooltip = {
        "html": "<b>Census Tract #:</b> {census_tract}<br><b>% Upward Mobility:</b> {mob}",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    }
        
    layer = pdk.Layer(
        "ColumnLayer",
        data,
        get_position="[lon, lat]",
        get_elevation="mob",
        auto_highlight=True,
        get_fill_color=[0, 100, 250 ],  
        elevation_scale=200,  # Adjusted for visibility
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
def render_edu_map(data):
    tooltip = {
        "html": "<b>Census Tract #:</b> {census_tract}<br><b>% People With >= GED:</b> {edu}",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    }
        
    layer = pdk.Layer(
        "ColumnLayer",
        data,
        get_position="[lon, lat]",
        get_elevation="edu",
        auto_highlight=True,
        get_fill_color=[210, 0, 100 ],  
        elevation_scale=20,  # Adjusted for visibility
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
st.subheader("Guadalupe, AZ was established by Yaqui Indians fleeing persecution and land dispossession under Mexican President Porfirio Díaz's policies in the late 19th and early 20th centuries. The community managed to preserve its unique cultural and geographical identity despite the pressures of urban expansion from neighboring Phoenix. Supported by missionaries and sympathetic locals, Guadalupe evolved into a vibrant enclave that retains its Yaqui heritage while also integrating Mexican-American influences.")
st.divider()
st.header("The Yaqui Migration")
st.subheader("Upon the Spaniards first contact with the Yaqui in 1533, the Yaqui occupied a 2500km2 territory in the Rio Yaqui valley. Within 200 years, as a result of Spanish settler colonial pressures, this range was reduced to 8 pueblos around the Yaqui River, accompanied by a radical transformation towards the Yaqui culture that can be observed today. The contemporary concept of the Yaqui community was evolved through continual prosperity with the Jesuit missions of the Spaniards. What transpired was an exemplar of Ortiz’s notion of transculturism, where Yaqui culture fused with Jesuit teachings to form a niche-synthesized religion. The eight 19th century-era Pueblos were a direct result of this new identity, and provided a backdrop for a overall Yaqui transformation towards economic, political, and religious autonomy. During the early 20th century, the Mexican Dictatorship's policies of extermination and deportation led to the Yaqui diaspora to the 5 primary U.S. locations shown below:")
ipcData, arcData, mobData, eduData = load_data()
render_migration_map(arcData)
st.divider()
st.header("Regional Socioeconomic Data")

st.subheader("The current location of Guadalupe, accompanied by its current problems, stems from the relocation of the Yaqui migrants from the settlement's original location. As a result of the second-class treatment of the Yaqui's in the early Arizona territory, a water dispute arose during the creation of the Salt Lake River Project. Consequently, the Yaquis were forced off their original land, and put on a ‘waterlogged’ and ‘undesirable’ tract of land for which the Federal government approved for the official establishment of the Town of Guadalupe. This nature of the land led to the loss of Yaqui traditional livelihood of agriculture, and consequently forced many Guadalupe residents to be exploited in the construction of the underlying canal and irrigation systems crucial to Phoenix’s current size. Yaqui were seen as expendable workers, living in dire and often deadly conditions, which continued throughout the entirety of the 20th century, culminating with the effects of the controvertial Bracero program. Further, the Yaqui became entirely dependent on the Anglo economy surrounding them, leading to severe poverty when Anglo interactions or opportunities declined. These socioeconomic inequalities and issues have been further propagated, leading to the disparate conditions in Guadalupe compared to its geographically adjacent communities. These inequalities and disparities can be clearly seen in the data visualizations below:")
row1_1, row1_2, row1_3 = st.columns(3)
with row1_1:
    st.header("Local Income Per Capita Comparison")
    render_ipc_map(ipcData)
    st.subheader("Census 2022; Policy Map")
with row1_2:
    st.header("Hispanic Upward Economic Mobility")
    render_mob_map(mobData)
    st.subheader("Census 2010; Policy Map")
with row1_3:
    st.header("Hispanic Educational Acquisiton GED+")
    render_edu_map(eduData)
    st.subheader("Census 2022; Policy Map")
st.divider()
st.header("Guadalupe: In Color")
st.subheader("Throughout the entirety of this course, we have learned that there are multiple ways to represent a community. From my past experiences in Guadalupe and my research of the roots of the community, the images and locations depicted below offer a more 'comprehensive' view of the community and its colorful/vibrant nature that many Phoenicians are not aware of. However, as a continuation of the previous section, I hope to provide a visual contrast between Guadalupe and one of its surrounding landmarks.")
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Religious Center", "Del Yaqui Restaurant", "Mercado de Guadalupe", "AZ Grand Resort", "Guadalupe Cemetary"])
with tab1:
    st.image('church.jpg', width=720, caption='Sourced From: https://outpostmagazine.com/guadalupe-arizona-a-forgotten-town-phoenix/')
    st.subheader('The primary attraction and religious center of the town is the Our Lady of Guadalupe Church. The Church, which is made up of two nearly identical buildings, offers services in English & Spanish within one church, and Yaqui in the other. In front of the churches lies a vacant lot of stagnant dust that makes up a significant percentage of the towns small territory. During Lent, the Yaqui community perform the traditional "deer dance" on this lot, which invites any and all to watch, but prohibits photography. ')
with tab2:
    st.image('delyaqui.png', width=720, caption='Sourced From: Google Maps Images')
    st.subheader('Del Yaqui, a colorful restaurant located near the Guadalupe Mercado is one of the only restaurants in Arizona focusing on Yaqui/Mexican cuisine. ')
with tab3:
    st.image('mercado.jpg', width=720, caption='Sourced From: https://outpostmagazine.com/guadalupe-arizona-a-forgotten-town-phoenix/')
    st.subheader('A vibrant community center of the town of Guadalupe, the Mercado offers a marketplace for organic hispanic foods/produce, in addition to some of the best casual,traditional food that Phoenix has to offer. ')
with tab4:
    st.image('azgrand.png', width=720, caption='Sourced From: Arizona Grand Resort & Spa Promotional Imaging')
    st.subheader('The AZ Grand Resort is an extremely commonly visited luxory resort nestled between the chaos of Downtown Phoenix, and right across from the town of Guadalupe. The splendor and luxory of the resort directly contrasts with the squalor and housing crises being experienced in the town of Guadalupe, highlighting the inequality. ')
with tab5:
    st.image('cemetary.jpg', width=720, caption='Sourced From: https://www.atlasobscura.com/places/guadalupe-cemetery')
    st.subheader('The Guadalupe Cemetary, one of the long-standing marks of the Yaqui Indian diaspora to the Phoenix, AZ region dates back to 1904. Due to land and water disputes with other Arizonan cities, the Yaqui settlement relocated to current day Guadalupe.')
st.divider()
st.header("Map Page Sources")



