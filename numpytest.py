import streamlit as st
import pandas as pd
import numpy as np
import csv
test = [0, 0]
progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
last_rows = np.random.randn(1, 1)
chart = st.line_chart()
with open('indego-trips-2021-q1.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        test.insert(1, row['duration'])
        test.pop(2)
        chart.add_rows(test)
        test.insert(0, row['duration'])
        test.pop(1)

st.button("Re-run")
