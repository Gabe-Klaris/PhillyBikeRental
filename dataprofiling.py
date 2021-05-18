import pandas as pd
import pandas_profiling
bike_data = pd.read_csv("indego-trips-2021-q1.csv")
#profile = bike_data.profile_report(title='Pandas Profiling Report')
#profile.to_file(output_file="dataprofile.html")
#put these values into a list:
#splice the lines to just a day
#take in a certain value for time (0:00 < x < 00:30)
#how many in first list = bikes taken out
#How many in second list = bikes put in 
start_times = bike_data.loc[bike_data.start_station == 3125, "start_time"]
end_times = bike_data.loc[bike_data.end_station == 3125, "end_time"]
daily_trips_end = []
halfhourtrip_end = []
daily_trips_start = []
halfhourtrip_start = []
day = "1/21/2021"
start_time = 1800
end_time = 1830
for i in start_times:
    if i.find(day) != -1:
        name = i.split(" ", 1)
        daily_trips_start.append(name[1])
for i in daily_trips_start:
    value = i.replace(":", "")
    time = int(value)
    if time >= start_time and time <= end_time:
        halfhourtrip_start.append(time)

for i in end_times:
    if i.find(day) != -1:
        name1 = i.split(" ", 1)
        daily_trips_end.append(name[1])
for i in daily_trips_end:
    value1 = i.replace(":", "")
    time1 = int(value1)
    if time1 >= start_time and time1 <= end_time:
        halfhourtrip_start.append(time)


print("within the half hour" , len(halfhourtrip_start) - len(halfhourtrip_end), "bike(s) were taken taken from the station")
    

