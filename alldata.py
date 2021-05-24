from datetime import datetime
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
full_data_1 = trip_data_2020_2.set_index("start_station").join(station_data.set_index("Station_ID"))
full_data_end_1 = trip_data_2020_2.set_index("end_station").join(station_data.set_index("Station_ID"))
full_data_2 = trip_data_2019_2.set_index("start_station").join(station_data.set_index("Station_ID"))
full_data_end_2 = trip_data_2019_2.set_index("end_station").join(station_data.set_index("Station_ID"))
web_byte = urlopen(req).read()
webpage = web_byte.decode('utf-8')
dates_2020_Q2 = pd.date_range(start="2020/04/01", end="2020/06/30", freq="D")
dates_2019_Q2 = pd.date_range(start="2019/04/01", end="2019/06/30",freq="D")
times_before = pd.date_range(start="1/1/2020",periods=49,freq="0h30min")
times = []
for i in times_before:
    timeStr = i.strftime("%H:%M")
    times.append(timeStr)
dates_list_2020 = []
dates_list_2019 = []
to_select = []
for i in dates_2020_Q2:
    timestampStr = i.strftime("%m-%d-%Y")
    dates_list_2020.append(timestampStr.replace("-",""))
for i in dates_2019_Q2:
    timestampStr = i.strftime("%m-%d-%Y")
    dates_list_2019.append(timestampStr.replace("-",""))
#select a date in the next two weeks
#show the half hour data from that day (day of the week) in the last two years 
d = datetime.today()
d_str = d.strftime("%m-%d-%Y")
selection = pd.date_range(start=d, periods=14,freq="D")
for i in selection:
    timesStr = i.strftime("%m-%d-%Y")
    to_select.append(timesStr)
selected_date = st.sidebar.selectbox("Pick a date", to_select)
selected_station = st.sidebar.selectbox("Pick a location", station_data["Station_Name"])
#making list of all times in the same quarter withnin the 2 years
start_times = []
start_times1 = full_data_1.loc[full_data_1.Station_Name ==selected_station, "start_time"]
start_times2 = full_data_2.loc[full_data_2.Station_Name ==selected_station, "start_time"]
for i in start_times1:
    start_times.append(i)
for i in start_times2:
    start_times.append(i)
end_times = []
end_times1 = full_data_end_1.loc[full_data_end_1.Station_Name ==selected_station, "end_time"]
end_times2 = full_data_end_2.loc[full_data_end_2.Station_Name ==selected_station, "end_time"]
for i in end_times1:
    end_times.append(i)
for i in end_times2:
    end_times.append(i)
#getting date for last year and year before
selected_date_2020 = int(selected_date.replace("-","")) -1 
selected_date_2019 = int(selected_date.replace("-","")) -2
selected_date_2019= "0" + str(selected_date_2019)
selected_date_2020= "0" + str(selected_date_2020)
date_2019 = dates_list_2019[dates_list_2019.index(selected_date_2019)+3]
date_2020 = dates_list_2020[dates_list_2020.index(selected_date_2020)+1]
day_trip_start_2020 = []
day_trip_start_2019 = []
day_trip_end_2020 = []
day_trip_end_2019 = []
date_2020_month = date_2020[0:2]
date_2020_day = date_2020[2:4]
date_2019_month = date_2019[0:2]
date_2019_day = date_2019[2:4]
for i in start_times:
    trips_list = i.split(" ")
    if "2020" in trips_list[0]:
        parts_list = trips_list[0].split("/")
        if (int(parts_list[0]) == int(date_2020_month)) and (int(parts_list[1])== int(date_2020_day)):
            day_trip_start_2020.append(trips_list[1])
    elif "2019" in trips_list[0]:
        parts_list1 = trips_list[0].split("-")
        if (int(parts_list1[1]) == int(date_2019_month)) and (int(parts_list1[2]) == int(date_2019_day)):
            day_trip_start_2019.append(trips_list[1])
for i in end_times:
    trips_list = i.split(" ")
    if "2020" in trips_list[0]:
        parts_list = trips_list[0].split("/")
        if (int(parts_list[0]) == int(date_2020_month)) and (int(parts_list[1])== int(date_2020_day)):
            day_trip_end_2020.append(trips_list[1])
    elif "2019" in trips_list[0]:
        parts_list1 = trips_list[0].split("-")
        if (int(parts_list1[1]) == int(date_2019_month)) and (int(parts_list1[2]) == int(date_2019_day)):
            day_trip_end_2019.append(trips_list[1])
halfhour_2020_netchange = [0]
halfhour_2019_netchange = [0]
for i in range (0,48):
    start_time = int(times[i].replace(":",""))
    end_time = int(times[i+1].replace(":",""))
    trip_2020_start_counter = 0
    trip_2019_start_counter = 0
    trip_2020_end_counter = 0
    trip_2019_end_counter = 0
    for i in day_trip_start_2020:
        trip_time = int(i.replace(":", ""))
        if (trip_time >= start_time) and (trip_time <= end_time):
            trip_2020_start_counter += 1
    for i in day_trip_start_2019:
        trip_2019_list = i.split(":")
        trip_time = int(trip_2019_list[0] + trip_2019_list[1])
        if (trip_time >= start_time) and (trip_time <= end_time):
            trip_2019_start_counter += 1
    for i in day_trip_end_2020:
        trip_time = int(i.replace(":", ""))
        if (trip_time >= start_time) and (trip_time <= end_time):
            trip_2020_end_counter += 1
    for i in day_trip_end_2019:
        trip_2019_list = i.split(":")
        trip_time = int(trip_2019_list[0] + trip_2019_list[1])
        if (trip_time >= start_time) and (trip_time <= end_time):
            trip_2019_end_counter += 1
    halfhour_2020_netchange.append(trip_2020_end_counter- trip_2020_start_counter)
    halfhour_2019_netchange.append(trip_2019_end_counter- trip_2019_start_counter)
times_ticks = []
for i in range(0,48):
    times_ticks.append(times[i] + "-" + times[i+1])
fig = plt.figure()
ax = plt.axes()
x_values = np.arange(1, len(times_ticks) +1, 1)
plt.xticks(x_values, times_ticks)
ax.tick_params(axis='x', rotation=70, labelsize=3)
plt.xlabel("Time")
plt.ylabel("Net change in bikes per half hour")
plt.title("Trips in 2020")
plt.plot(halfhour_2020_netchange)
st.pyplot(fig)
#create graph for trips ended
fig1 = plt.figure()
ax1 = plt.axes()
plt.xticks(x_values, times_ticks)
plt.title("Trips in 2019")
plt.xlabel("Time")
plt.ylabel("Net change in bikes per half hour")
ax1.tick_params(axis='x', rotation=70, labelsize=3)
plt.plot(halfhour_2019_netchange)
st.pyplot(fig1)
        
#clean up and combine with other


#what is an api call??
#tf is this>
