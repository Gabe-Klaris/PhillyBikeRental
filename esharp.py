import streamlit as st
import numpy as np
import pandas as pd

st.title("This is a test")
st.write("Hello wrold")
map_data = pd.DataFrame(
    np.random.randn(1, 2) / [50, 50] + [39.95, -75.16],
    columns=['lat', 'lon'])
st.write(np.random.randn(1, 2) / [50, 50] + [39.95, -75.16])
st.map(map_data)



