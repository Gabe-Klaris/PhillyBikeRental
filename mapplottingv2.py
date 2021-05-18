import streamlit as st
from urllib.request import Request, urlopen
import urllib
import pandas as pd
import re
import json
stuff = "https://kiosks.bicycletransit.workers.dev/phl"
req = Request(stuff, headers={'User-Agent': 'Mozilla/5.0'})
trip_data = pd.read_csv("indego-trips-2021-q1.csv")
station_data = pd.read_csv("indego-stations-2021-01-01.csv")
full_data = trip_data.set_index("start_station").join(station_data.set_index("Station_ID"))
print(station_data.loc[station_data.Station_ID == 3125, "Station_Name"])
url = "https://kiosks.bicycletransit.workers.dev/phl"
# with urllib.request.urlopen(req) as url:
#     data = json.loads(url.read().decode())
# for key, value in data.items():
#     print(key)
# print(data['type'])

