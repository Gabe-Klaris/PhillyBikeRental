import streamlit as st
from urllib.request import Request, urlopen
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import plotly.express as px
import holidays
#file opening
stuff = "https://kiosks.bicycletransit.workers.dev/phl"
req = Request(stuff, headers={'User-Agent': 'Mozilla/5.0'})
trip_data_2021_1 = pd.read_csv("indego-trips-2021-q1.csv")
trip_data_2020_4 = pd.read_csv("indego-trips-2020-q4.csv")
trip_data_2020_3 = pd.read_csv("indego-trips-2020-q3.csv")
trip_data_2020_2 = pd.read_csv("indego-trips-2020-q2.csv")
trip_data_2020_1 = pd.read_csv("indego-trips-2020-q1.csv")
trip_data_2019_1 = pd.read_csv("indego-trips-2019-q1.csv")
trip_data_2019_2 = pd.read_csv("indego-trips-2019-q2.csv")
trip_data_2019_3 = pd.read_csv("indego-trips-2019-q3.csv")
trip_data_2019_4 = pd.read_csv("indego-trips-2019-q4.csv")
station_data = pd.read_csv("indego-stations-2021-01-01.csv")
dates = pd.read_csv("Dates.csv")
full_data = trip_data_2021_1.set_index("start_station").join(station_data.set_index("Station_ID"))
full_data_end = trip_data_2021_1.set_index("end_station").join(station_data.set_index("Station_ID"))
web_byte = urlopen(req).read()
webpage = web_byte.decode('utf-8')
stations = list(station_data.loc[station_data.Status == "Active", "Station_Name"])
#creating date lists
dates_2020_Q2 = pd.date_range(start="2020/01/01", end="2020/12/31", freq="D")
dates_2019_Q2 = pd.date_range(start="2019/01/01", end="2019/12/31",freq="D")
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
#holidays
us_holidays = holidays.CountryHoliday('US', prov=None, state='PA')
#show the half hour data from that day (day of the week) in the last two years 
d = datetime.today()
d_str = d.strftime("%m-%d-%Y")
dayofweek = d.strftime("%A")
selection = pd.date_range(start=d, periods=14,freq="D")
for i in selection:
    timesStr = i.strftime("%m-%d-%Y")
    to_select.append(timesStr)
#streamlit sidebar markdown + prompts to show data for
st.sidebar.markdown("# Pick a location to show data for")
selected_answer = st.sidebar.selectbox("Pick a location", stations)
st.sidebar.markdown("# Select a date range to show trip data for")
start_date = st.sidebar.selectbox("Pick a start date", dates["Dates"])
end_date = st.sidebar.selectbox("Pick an end date", dates["Dates"])
st.sidebar.markdown("# Select a future (or the current) date to take out a bike on")
selected_date = st.sidebar.selectbox("Pick a date", to_select)
#list and dictionary defining for map
lat = []
lon = []
longitude = []
latitude = []
name_avaible = {}
better_webpage = webpage.split("\"type\":\"Feature\"},")
#getting bikes avaiable and more!
for i in range (145):
    single_part = better_webpage[i]
    single_part = single_part.split(",")
    bikes_available = 0
    for f in single_part:
        if f == "\"isAvailable\":true":
            bikes_available += 1
    #finding name
    name_part = better_webpage[i]
    startindx = name_part.find("name")
    endindx = name_part.find(",\"coordinates\"")
    stationName = name_part[startindx:endindx]
    stationNamecon = stationName[7:-1]
    #docks available
    startindx1 = name_part.find("\"docksAvailable\"")
    endindx1 = name_part.find("\"bikesAvailable\":")
    docks_avalable = name_part[startindx1:endindx1]
    docks_avalablecon = int(docks_avalable[17:-1])
    #classic bikes
    startindx2 = name_part.find("classicBikesAvailable")
    endindx2 = name_part.find("\"smartBikesAvailable\":")
    classic_bikes_avalable = name_part[startindx2:endindx2]
    classic_bikes_avalablecon = int(classic_bikes_avalable[23:-1])
    #electric bikes
    startindx3 = name_part.find("electricBikesAvailable")
    endindx3 = name_part.find("\"rewardBikesAvailable\":")
    electric_bikes_avalable = name_part[startindx3:endindx3]
    electric_bikes_avalablecon = int(electric_bikes_avalable[24:-1])
    name_avaible[stationNamecon] = bikes_available, docks_avalablecon, classic_bikes_avalablecon,electric_bikes_avalablecon
#list of all stations lat + lon and bike data
names = []
bikes_amount = []
docks = []
classic = []
electric = []
for i in stations[1:]:
    bruh = list(full_data[full_data["Station_Name"] == i].index)
    bruh1 = list(trip_data_2021_1.loc[trip_data_2021_1.start_station == bruh[0], "start_lat"])
    bruh2 = bruh1[0]
    latitude.append(bruh2)
    names.append(i)
    if i == "Broad & Passyunk" or i == "11th & Market":
        bikes_amount.append(name_avaible[i + " "][0])
        docks.append(name_avaible[i + " "][1])
        classic.append(name_avaible[i + " "][2])
        electric.append(name_avaible[i + " "][3])
    else:
        bikes_amount.append(name_avaible[i][0])
        docks.append(name_avaible[i][1])
        classic.append(name_avaible[i][2])
        electric.append(name_avaible[i][3])
for i in stations[1:]:
    bruh = list(full_data[full_data["Station_Name"] == i].index)
    bruh1 = list(trip_data_2021_1.loc[trip_data_2021_1.start_station == bruh[0], "start_lon"])
    bruh2 = bruh1[0]
    longitude.append(bruh2)
stations_coords = list(zip(latitude, longitude,names,bikes_amount,docks,classic,electric))
all_points = pd.DataFrame(
    stations_coords,
    columns=['lat', 'lon','station_name','Bikes Available','Docks Available','Classic Bikes Available', 'Electric Bikes Available']
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
    if (start_date_month > start_month and start_date_month < end_month) or (start_date_month > start_month and start_date_month == end_month and start_date_day <= end_day) or (start_date_month == start_month and start_date_month < end_month and start_date_day >= start_day) or (start_date_month >= start_month and start_date_month <= end_month and start_date_day >= start_day and start_date_day <= end_day):
        for j in start_times:
            trip_date = j.split(" ")
            trip_day = trip_date[0]
            if i == trip_day:
                trips_per_day += 1
        average_trips_start.append(trips_per_day)
#gets the amount of trips ended in a day and appends the number to a list
for f in dates["Dates"]:
    trips_per_day1 = 0
    list_date1 = f.split("/")
    end_date_month = int(list_date1[0])
    end_date_day = int(list_date1[1])
    if (end_date_month > start_month and end_date_month < end_month) or (end_date_month > start_month and end_date_month == end_month and end_date_day <= end_day) or (end_date_month == start_month and end_date_month < end_month and end_date_day >= start_day) or (end_date_month >= start_month and end_date_month <= end_month and end_date_day >= start_day and end_date_day <= end_day):
        for h in end_times:
            trip_date1 = h.split(" ")
            trip_day1 = trip_date1[0]
            if f == trip_day1:
                trips_per_day1 += 1
        average_trips_end.append(trips_per_day1)
#getting date for last year and year before and trips in that day
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
date_form_2020 = date_2020_month + "/" + date_2020_day + "/" + "2020"
date_form_2019 = date_2019_month + "/" + date_2019_day + "/" + "2019"
quarter_2020 = int(date_2020_month + date_2020_day)
quarter_2019 = int(date_2019_month + date_2019_day)
if quarter_2020 >= 101 and quarter_2020 <= 331:
    full_data_1 = trip_data_2020_1.set_index("start_station").join(station_data.set_index("Station_ID"))
    full_data_end_1 = trip_data_2020_1.set_index("end_station").join(station_data.set_index("Station_ID"))
if quarter_2020 >= 401 and quarter_2020 <= 630:
    full_data_1 = trip_data_2020_2.set_index("start_station").join(station_data.set_index("Station_ID"))
    full_data_end_1 = trip_data_2020_2.set_index("end_station").join(station_data.set_index("Station_ID"))
if quarter_2020 >= 701 and quarter_2020 <= 930:
    full_data_1 = trip_data_2020_3.set_index("start_station").join(station_data.set_index("Station_ID"))
    full_data_end_1 = trip_data_2020_3.set_index("end_station").join(station_data.set_index("Station_ID"))
if quarter_2020 >= 1001 and quarter_2020 <= 1231:
    full_data_1 = trip_data_2020_4.set_index("start_station").join(station_data.set_index("Station_ID"))
    full_data_end_1 = trip_data_2020_4.set_index("end_station").join(station_data.set_index("Station_ID"))
if quarter_2019 >=101 and quarter_2019 <= 331:
    full_data_2 = trip_data_2019_1.set_index("start_station").join(station_data.set_index("Station_ID"))
    full_data_end_2 = trip_data_2019_1.set_index("end_station").join(station_data.set_index("Station_ID"))
if quarter_2019 >=401 and quarter_2019 <= 630:
    full_data_2 = trip_data_2019_2.set_index("start_station").join(station_data.set_index("Station_ID"))
    full_data_end_2 = trip_data_2019_2.set_index("end_station").join(station_data.set_index("Station_ID"))
if quarter_2019 >=701 and quarter_2019 <= 930:
    full_data_2 = trip_data_2019_3.set_index("start_station").join(station_data.set_index("Station_ID"))
    full_data_end_2 = trip_data_2019_3.set_index("end_station").join(station_data.set_index("Station_ID"))
if quarter_2019 >=1001 and quarter_2019 <= 1231:
    full_data_2 = trip_data_2019_4.set_index("start_station").join(station_data.set_index("Station_ID"))
    full_data_end_2 = trip_data_2019_4.set_index("end_station").join(station_data.set_index("Station_ID"))
#making list of all times in the same quarter withnin the 2 years
start_times = []
start_times1 = full_data_1.loc[full_data_1.Station_Name ==selected_answer, "start_time"]
start_times2 = full_data_2.loc[full_data_2.Station_Name ==selected_answer, "start_time"]
for i in start_times1:
    start_times.append(i)
for i in start_times2:
    start_times.append(i)
end_times = []
end_times1 = full_data_end_1.loc[full_data_end_1.Station_Name ==selected_answer, "end_time"]
end_times2 = full_data_end_2.loc[full_data_end_2.Station_Name ==selected_answer, "end_time"]
for i in end_times1:
    end_times.append(i)
for i in end_times2:
    end_times.append(i)
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
#getting average
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
#setting up ticks
times_ticks = []
for i in range(0,48):
    times_ticks.append(times[i] + " - " + times[i+1])
#display map data + amount of bikes available guau so efficent u so cool
st.header("Map of all stations and current data from the stations")
fig = px.scatter_mapbox(all_points, lat="lat", lon="lon", hover_name="station_name",hover_data=["Bikes Available",'Docks Available','Classic Bikes Available', 'Electric Bikes Available'], color_discrete_sequence=["fuchsia"], zoom=3, height=300)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(figure_or_data=fig, use_container_width=True)
#checks if the range of dates is valid if not/ lists will be empty so no data
if int_start_date <= int_end_date:
    st.header("Trips ended and started at " + selected_answer + " between " + start_date + " and " + end_date)
    dates_list = []
    for i in range(dates[dates.Dates == start_date].index[0], dates[dates.Dates == end_date].index[0] + 1):
        dates_list.append(dates.loc[i, "Dates"])
    holidays = []
    for i in range(0,len(dates_list)):
        if dates_list[i] in us_holidays:
            holidays.append(dates_list[i] + " " + us_holidays.get(dates_list[i]))
    #creating trips started graph
        if i == "2/14/2021":
            holidays.append(dates_list[i] + " Valentine's Day")
        if i == "2/17/2021":
            holidays.append(dates_list[i] + " St. Patrick's Day")
    st.write("The holidays for this date range are:")
    for i in holidays:
        st.write(i)
    fig = plt.figure()
    ax = plt.axes()
    x_values = np.arange(1, 2 + dates[dates.Dates == end_date].index[0]-dates[dates.Dates == start_date].index[0], 1)
    plt.xticks(x_values, dates_list)
    ax.tick_params(axis='x', rotation=70, labelsize=3)
    plt.xlabel("Days")
    plt.title("Trips started")
    plt.plot(average_trips_start)
    st.pyplot(fig)
    #create graph for trips ended
    fig1 = plt.figure()
    ax1 = plt.axes()
    plt.xticks(x_values, dates_list)
    plt.title("Trips ended")
    plt.xlabel("Days")
    ax1.tick_params(axis='x', rotation=70, labelsize=3)
    plt.plot(average_trips_end)
    st.pyplot(fig1)

else:
    st.write("Select new end date//can't be before start date")
#graphing half hour graphs
st.header("Based on the date you want to take a bike out on, these graphs show data from each half hour on the same " + dayofweek + " in 2020 and 2019")
fig = plt.figure()
ax = plt.axes()
x_values = np.arange(1, len(times_ticks) +1, 1)
plt.xticks(x_values, times_ticks)
ax.tick_params(axis='x', rotation=70, labelsize=5)
plt.xlabel("Time")
plt.ylabel("Net change in bikes per half hour")
plt.title("Trips in 2020")
plt.plot(halfhour_2020_netchange)
st.pyplot(fig)
#display if date is holiday
if date_form_2020 in us_holidays:
    st.write(us_holidays.get(date_form_2020))
#create graph for trips ended
fig1 = plt.figure()
ax1 = plt.axes()
plt.xticks(x_values, times_ticks)
plt.title("Trips in 2019")
plt.xlabel("Time")
plt.ylabel("Net change in bikes per half hour")
ax1.tick_params(axis='x', rotation=70, labelsize=5)
plt.plot(halfhour_2019_netchange)
st.pyplot(fig1)
#will display if date is holiday
if date_form_2019 in us_holidays:
    st.write(us_holidays.get(date_form_2019))
st.write("""The y axis (Net change in bikes per half hour) is calculated by subtracting the trips that ended
at the station by the trips that ended at the station during the half hour peroid. This number will be
the overall net change in bikes available at the station through the half hour. This also means that
this number does not calculate the activity of the station as a value of \"0\" could mean that
five trips started and ended at the station or that nobody used the station in the half hour.""")
#finish combining all data then work seperately on the clicky stuff with link
#change to fit with data within past two years.
#headers and stuff
#explain net change in bikes