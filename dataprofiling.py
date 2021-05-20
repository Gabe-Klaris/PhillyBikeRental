import pandas as pd
import pandas_profiling
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
dates = pd.read_csv("Dates.csv")
bike_data = pd.read_csv("indego-trips-2021-q1.csv")
station_data = pd.read_csv("indego-stations-2021-01-01.csv")
full_data = bike_data.set_index("start_station").join(station_data.set_index("Station_ID"))
full_data_end = bike_data.set_index("end_station").join(station_data.set_index("Station_ID"))
st.sidebar.markdown("# Pick a location and a time period")
selected_answer = st.sidebar.selectbox("Pick a location to display data for", station_data["Station_Name"])
start_date = st.sidebar.selectbox("Pick a start date", dates["Dates"])
end_date = st.sidebar.selectbox("Pick an end date", dates["Dates"])

#station_id = station_data.loc[station_data.Station_Name == selected_answer, "Station_ID"]
#profile = bike_data.profile_report(title='Pandas Profiling Report')
#profile.to_file(output_file="dataprofile.html")
#put these values into a list:
#splice the lines to just a day
#take in a certain value for time (0:00 < x < 00:30)
#how many in first list = bikes taken out
#How many in second list = bikes put in 

start_times = full_data.loc[full_data.Station_Name == selected_answer, "start_time"]
end_times = full_data_end.loc[full_data_end.Station_Name == selected_answer, "end_time"]

average_trips_start = []
average_trips_end = []
halfhourtrip_end = []
daily_trips_start = []
halfhourtrip_start = []
#getting all dates into a list
list_start_date = start_date.split("/")
start_month = int(list_start_date[0])
start_day = int(list_start_date[1])
list_end_date = end_date.split("/")
end_month = int(list_end_date[0])
end_day = int(list_end_date[1])
for i in dates["Dates"]:
    trips_per_day = 0
    list_date = i.split("/")
    start_date_month = int(list_date[0])
    start_date_day = int(list_date[1])
    if start_date_month >= start_month and start_date_month <= end_month and start_date_day >= start_day and start_date_day <= end_day:
        for j in start_times:
            trip_date = j.split(" ")
            trip_day = trip_date[0]
            if i == trip_day:
                trips_per_day += 1  
        average_trips_start.append(trips_per_day)
st.write(average_trips_start)
for f in dates["Dates"]:
    trips_per_day1 = 0
    list_date1 = f.split("/")
    end_date_month = int(list_date1[0])
    end_date_day = int(list_date1[1])
    if end_date_month >= start_month and end_date_month <= end_month and end_date_day >= start_day and end_date_day <= end_day:
        for h in end_times:
            trip_date1 = h.split(" ")
            trip_day1 = trip_date1[0]
            if f == trip_day1:
                trips_per_day1 += 1
        average_trips_end.append(trips_per_day1)
st.write(average_trips_end)
# chartdata_start = figure(
#     title = "Line",
#     x_axis_label = "Day",
#     y_axis_label= "Bikes Taken out"
# )
start = dates["Dates"].str.index(start_date)
if  end_date_month >= start_date_month and end_date_day >= start_date_day:
    dates_list = []
    #start at index of start_date end at len of list
    for i in range (start_date , len(average_trips_start)):
        dates_list.append(dates.loc[i, "Dates"])
    fig = plt.figure()
    ax = plt.axes()
    x_values = np.arange(1, len(average_trips_start) + 1, 1)
    plt.xticks(x_values, dates_list)
    plt.xlabel("Days")
    plt.plot(average_trips_start)
    st.pyplot(fig)
    #need to create graph for trips ended
    #might need to fix line starting at wrong point?
else:
    st.write("Select new end date//can't be before start date")
# start_time = 1800
# end_time = 1830
# for i in start_times:
#     trip_date = i.split(" ")
#     int_trip_date = int(trip_date[0].replace("/", ""))
#     if int_trip_date >= int_start_date and int_trip_date <= int_end_date:
#         daily_trips_start.append([1])
# for i in daily_trips_start:
#     value = i.replace(":", "")
#     time = int(value)
#     if time >= start_time and time <= end_time:
#         halfhourtrip_start.append(time)

# for i in end_times:
#     if i.find(day) != -1:
#         name1 = i.split(" ", 1)
#         daily_trips_end.append(name[1])
# for i in daily_trips_end:
#     value1 = i.replace(":", "")
#     time1 = int(value1)
#     if time1 >= start_time and time1 <= end_time:
#         halfhourtrip_start.append(time)
#put on streamlit
#have the user selcted any period of days within the quarter
#average all the half hour peroids within a day/ divide 
#display data/ day of the week on the graph 

#st.write("within the half hour" , len(halfhourtrip_start) - len(halfhourtrip_end), "bike(s) were taken taken from the station")
    

