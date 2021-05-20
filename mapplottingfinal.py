import streamlit as st
from urllib.request import Request, urlopen
import pandas as pd
import re
import json
import pydeck as pdk
import matplotlib.pyplot as plt
import numpy as np
#file opening
stuff = "https://kiosks.bicycletransit.workers.dev/phl"
req = Request(stuff, headers={'User-Agent': 'Mozilla/5.0'})
trip_data_2021_1 = pd.read_csv("indego-trips-2021-q1.csv")
trip_data_2020_4 = pd.read_csv("indego-trips-2020-q4.csv")
trip_data_2020_3 = pd.read_csv("indego-trips-2020-q3.csv")
trip_data_2020_2 = pd.read_csv("indego-trips-2020-q2.csv")
trip_data_2019_1 = pd.read_csv("indego-trips-2019-q1.csv")
trip_data_2019_2 = pd.read_csv("indego-trips-2019-q2.csv")
trip_data_2019_3 = pd.read_csv("indego-trips-2019-q3.csv")
trip_data_2019_4 = pd.read_csv("indego-trips-2019-q4.csv")
trip_data = pd.read_csv("indego-trips-2020-q1.csv")
station_data = pd.read_csv("indego-stations-2021-01-01.csv")
dates = pd.read_csv("Dates.csv")
full_data = trip_data.set_index("start_station").join(station_data.set_index("Station_ID"))
full_data_end = trip_data.set_index("end_station").join(station_data.set_index("Station_ID"))
web_byte = urlopen(req).read()
webpage = web_byte.decode('utf-8')
#streamlit sidebar markdown + prompts to show data for
st.sidebar.markdown("# Pick a location and it will show the bikes available and location and the past data for the station")
selected_answer = st.sidebar.selectbox("# Pick a location", station_data["Station_Name"])
start_date = st.sidebar.selectbox("Pick a start date", dates["Dates"])
end_date = st.sidebar.selectbox("Pick an end date", dates["Dates"])
#list and dictionary defining for map
lat = []
lon = []
longitude = []
latitude = []
name_avaible = {}
better_webpage = webpage.split("\"type\":\"Feature\"},")
#getting bikes avaiable
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
    name_avaible[stationNamecon] = bikes_available
trip_data.dropna(0, inplace=True)
#list of all stations lat + lon
for i in trip_data["start_lat"]:
    if i not in latitude:
        latitude.append(float(i))
for i in trip_data["start_lon"]:
    if i not in longitude:
        longitude.append(float(i))
latitude.pop(0)
longitude.pop(0)
stations_coords = list(zip(latitude, longitude))
all_points = pd.DataFrame(
    stations_coords,
    columns=['lat', 'lon']
)
#for graphs
#all the start and end times at a station
start_times = full_data.loc[full_data.Station_Name ==selected_answer, "start_time"]
end_times = full_data_end.loc[full_data_end.Station_Name ==selected_answer, "end_time"]
#line would start at 0, then at first date this zero is for 0,0 so the first data point doesnt start before first date
average_trips_start = [0]
average_trips_end = [0]
#creating int values for dates
#split the date for start and end into ints month and day
list_start_date = start_date.split("/")
start_month = int(list_start_date[0])
start_day = int(list_start_date[1])
list_end_date = end_date.split("/")
end_month = int(list_end_date[0])
end_day = int(list_end_date[1])
int_start_date = int(start_date.replace("/", ""))
int_end_date = int(end_date.replace("/", ""))
#gets the amount of trips started in a day and appends the number to a list
for i in dates["Dates"]:
    trips_per_day = 0
    list_date = i.split("/")
    start_date_month = int(list_date[0])
    start_date_day = int(list_date[1])
    if (start_date_month > start_month and start_date_month < end_month) or (start_date_month > start_month and start_date_month == end_month and start_date_day <= end_day) or (start_date_month == start_month and start_date_month < end_month and start_date_day >= start_date) or (start_date_month >= start_month and start_date_month <= end_month and start_date_day >= start_day and start_date_day <= end_day):
        for j in start_times:
            trip_date = j.split(" ")
            trip_day = trip_date[0]
            if i == trip_day:
                trips_per_day += 1
        average_trips_start.append(trips_per_day)
#gets the amount of trips ended in a day and appends the number to a list
#gets the amount of trips ended in a day and appends the number to a list
for f in dates["Dates"]:
    trips_per_day1 = 0
    list_date1 = f.split("/")
    end_date_month = int(list_date1[0])
    end_date_day = int(list_date1[1])
    if (end_date_month > start_month and end_date_month < end_month) or (end_date_month > start_month and end_date_month == end_month and end_date_day <= end_day) or (end_date_month == start_month and end_date_month < end_month and end_date_day >= start_date) or (end_date_month >= start_month and end_date_month <= end_month and end_date_day >= start_day and end_date_day <= end_day):
        for h in end_times:
            trip_date1 = h.split(" ")
            trip_day1 = trip_date1[0]
            if f == trip_day1:
                trips_per_day1 += 1
        average_trips_end.append(trips_per_day1)
#display map data + amount of bikes available
if (selected_answer == "Virtual Station"):
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
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=39.953,
            longitude=-75.17,
            zoom=10,
            pinch=50,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=single_point,
                get_position='[lon, lat]',
                get_fill_color=[140, 200, 0],
                get_radius=100,
                get_line_color=[0, 0, 0],
            ),
            pdk.Layer(
                "ScatterplotLayer",
                data=all_points,
                get_position='[lon, lat]',
                get_fill_color=[255, 140, 0],
                get_radius=50,
            ),
        ],
    ))
    st.write("There are currently" , name_avaible[selected_answer] , "bikes available at this location")
#checks if the range of dates is valid if not/ lists will be empty so no data
if int_start_date <= int_end_date:
    dates_list = []
    for i in range(dates[dates.Dates == start_date].index[0], dates[dates.Dates == end_date].index[0] + 1):
        dates_list.append(dates.loc[i, "Dates"])
    #creating trips started graph
    fig = plt.figure()
    ax = plt.axes()
    x_values = np.arange(1, 2 + dates[dates.Dates == end_date].index[0]-dates[dates.Dates == start_date].index[0], 1)
    plt.xticks(x_values, dates_list)
    ax.tick_params(axis='x', rotation=70, labelsize=3)
    plt.xlabel("Days")
    plt.title("Trips started at the location")
    plt.plot(average_trips_start)
    st.pyplot(fig)
    #create graph for trips ended
    fig1 = plt.figure()
    ax1 = plt.axes()
    plt.xticks(x_values, dates_list)
    plt.title("Trips ended at the location")
    plt.xlabel("Days")
    ax1.tick_params(axis='x', rotation=70, labelsize=3)
    plt.plot(average_trips_end)
    st.pyplot(fig1)

else:
    st.write("Select new end date//can't be before start date")

#finish combining all data then work seperately on the clicky stuff with link
#change to fit with data within past two years.
