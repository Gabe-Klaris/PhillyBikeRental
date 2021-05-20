import pandas as pd
import pandas_profiling
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
#opening csv, getting user responces for dates and location
dates = pd.read_csv("Dates.csv")
bike_data = pd.read_csv("indego-trips-2021-q1.csv")
station_data = pd.read_csv("indego-stations-2021-01-01.csv")
trip_data_2020_4 = pd.read_csv("indego-trips-2020-q4.csv")
trip_data_2020_3 = pd.read_csv("indego-trips-2020-q3.csv")
trip_data_2020_2 = pd.read_csv("indego-trips-2020-q2.csv")
trip_data_2019_1 = pd.read_csv("indego-trips-2019-q1.csv")
trip_data_2019_2 = pd.read_csv("indego-trips-2019-q2.csv")
trip_data_2019_3 = pd.read_csv("indego-trips-2019-q3.csv")
trip_data_2019_4 = pd.read_csv("indego-trips-2019-q4.csv")
full_data = bike_data.set_index("start_station").join(station_data.set_index("Station_ID"))
full_data_end = bike_data.set_index("end_station").join(station_data.set_index("Station_ID"))
st.sidebar.markdown("# Pick a location and a time period")
selected_answer = st.sidebar.selectbox("Pick a location to display data for", station_data["Station_Name"])
start_date = st.sidebar.selectbox("Pick a start date", dates["Dates"])
end_date = st.sidebar.selectbox("Pick an end date", dates["Dates"])

#all the start and end times at a station
start_times = full_data.loc[full_data.Station_Name == selected_answer, "start_time"]
end_times = full_data_end.loc[full_data_end.Station_Name == selected_answer, "end_time"]
#line would start at 0, then at first date this zero is for 0,0 so the first data point doesnt start before first date
average_trips_start = [0]
average_trips_end = [0]
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
#checks if the range of dates is valid if not/ lists will be empty so no data
if  int_start_date <= int_end_date:
    dates_list = []
    #start at index of start_date end at index of end date
    for i in range(dates[dates.Dates == start_date].index[0], dates[dates.Dates == end_date].index[0] + 1):
        dates_list.append(dates.loc[i, "Dates"])
    #creating trips started graph
    fig = plt.figure()
    ax = plt.axes()
    x_values = np.arange(1, 2 + dates[dates.Dates == end_date].index[0]-dates[dates.Dates == start_date].index[0], 1)
    plt.xticks(x_values, dates_list)
    ax.tick_params(axis='x', rotation=70, labelsize = 3)
    plt.xlabel("Days")
    plt.title("Trips started at the location")
    plt.plot(average_trips_start)
    st.pyplot(fig)
    #need to create graph for trips ended
    fig1 = plt.figure()
    ax1 = plt.axes()
    #x_values1 = np.arange(1, 2 + dates[dates.Dates == end_date].index[0]-dates[dates.Dates == start_date].index[0], 1)
    plt.xticks(x_values, dates_list)
    plt.title("Trips ended at the location")
    plt.xlabel("Days")
    ax1.tick_params(axis='x', rotation=70, labelsize = 3)
    plt.plot(average_trips_end)
    st.pyplot(fig1)

else:
    st.write("Select new end date//can't be before start date")

#if you wanted to see the amount of trips within a certain half our
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
    
#data back the last two years
#https://pandas.pydata.org/docs/reference/api/pandas.date_range.html
