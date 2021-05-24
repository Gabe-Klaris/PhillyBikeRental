import streamlit as st
from urllib.request import Request, urlopen
import pandas as pd
import re
import json
import pydeck as pdk
import plotly.express as px
stuff = "https://kiosks.bicycletransit.workers.dev/phl"
req = Request(stuff, headers={'User-Agent': 'Mozilla/5.0'})
trip_data = pd.read_csv("indego-trips-2021-q1.csv")
station_data = pd.read_csv("indego-stations-2021-01-01.csv")
full_data = trip_data.set_index("start_station").join(station_data.set_index("Station_ID"))
web_byte = urlopen(req).read()
webpage = web_byte.decode('utf-8')
stations = list(station_data.loc[station_data.Status == "Active", "Station_Name"])
lat = []
lon = []
longitude = []
latitude = []
name_avaible = {}
better_webpage = webpage.split("\"type\":\"Feature\"},")
for i in range (145):
    single_part = better_webpage[i]
    single_part = single_part.split(",")
    bikes_available = 0
    for f in single_part:
        if f == "\"isAvailable\":true":
            bikes_available += 1
    name_part = better_webpage[i]
    startindx = name_part.find("name")
    endindx = name_part.find(",\"coordinates\"")
    stationName = name_part[startindx:endindx]
    stationNamecon = stationName[7:-1]
    #print(stationNamecon)
    name_avaible[stationNamecon] = bikes_available
#print(name_avaible)

##very ineffecent way of getting coordinates from website
# while(webpage.find("-75.") != -1):    
#     for i in range(2):
#         startinx = webpage.find("-75.")
#         if webpage[startinx + 9] == "3" or webpage[startinx + 9] ==  "9":
#             endinx = webpage.find("-75.") + 7
#         else: 
#             endinx = webpage.find("-75.") + 9
#         webpage = webpage[:startinx] + webpage[endinx:]
#     startinx = webpage.find("-75.")
#     if webpage[startinx + 9] == "3" or webpage[startinx + 9] == "9":
#         endinx = webpage.find("-75.") + 7
#     else: 
#         endinx = webpage.find("-75.") + 9
#     firstreplace = webpage[startinx: endinx].replace("}", "")
#     longitude.append(float(firstreplace.replace(",","")))

#     webpage = webpage[:startinx] + webpage[endinx:]
    
# while(webpage.find("39.") != -1):
#     for i in range(2):
#         startLinx = webpage.find("39.")
#         webpage = webpage[:startLinx] + webpage[startLinx + 8:]
#     startLinx = webpage.find("39.")
#     first = (webpage[startLinx: startLinx + 8].replace("}", ""))
#     second = (webpage[startLinx: startLinx + 8].replace("\"", ""))
#     latitude.append(float(second.replace(",","")))
#     webpage = webpage[:startLinx] + webpage[startLinx + 8:]
#coordinates = list(zip(latitude, longitude))
#print(better_webpage[0])
#for getting availability:
#seperate string after ""bikes"" then find start and end square bracket count for "isavaible":true
#then find someway to display this ## next to the matching station?
st.sidebar.markdown("# Pick a location and it will show the bikes available and location")
selected_answer = st.sidebar.selectbox("# Pick a location", station_data["Station_Name"])
names = []
data = []
for i in stations[1:]:
    bruh = list(full_data[full_data["Station_Name"] == i].index)
    bruh1 = list(trip_data.loc[trip_data.start_station == bruh[0], "start_lat"])
    bruh2 = bruh1[0]
    latitude.append(bruh2)
    names.append(i)
    data.append("yello")
for i in stations[1:]:
    bruh = list(full_data[full_data["Station_Name"] == i].index)
    bruh1 = list(trip_data.loc[trip_data.start_station == bruh[0], "start_lon"])
    bruh2 = bruh1[0]
    longitude.append(bruh2)
stations_coords = list(zip(latitude, longitude,names))
all_points = pd.DataFrame(
    stations_coords,
    columns=['lat', 'lon','station_name']
)
if selected_answer == "Virtual Station":
    st.write("No data here: only for drop offs")
else:
    lat1 = full_data.loc[full_data.Station_Name == selected_answer, "start_lat"]
    lon1 = full_data.loc[full_data.Station_Name == selected_answer, "start_lon"]
    lon.append(float(lon1.iloc[0]))
    lat.append(float(lat1.iloc[0]))
    coordinates = list(zip(lat, lon))
    single_point =pd.DataFrame(
        coordinates,
        columns = ['lat', 'lon']
        )
    fig = px.scatter_mapbox(all_points, lat="lat", lon="lon", hover_name="station_name", color_discrete_sequence=["fuchsia"], zoom=3, height=300)
    fig.update_layout(
    mapbox_style="white-bg",
    mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "sourceattribution": "United States Geological Survey",
            "source": [
                "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
            ]
        }
      ])
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(figure_or_data=fig, use_container_width=True)
    st.write("There are currently" , name_avaible[selected_answer] , "bikes available at this location")