import streamlit as st
import pandas as pd
import numpy as np

st.write('# Uber Pickups in NYC')

# load data
data = pd.read_csv('https://weichselbraun.net/ke-e/data/uber-pickups.csv.gz')
data['Date/Time'] = pd.to_datetime(data['Date/Time'])
print('hallo')

if st.checkbox('Show raw data'):
    st.write('## Raw data')
    st.write(data)

st.write('## Pickups per hour')
hist_values = np.histogram(data['Date/Time'].dt.hour, bins=24, range=(0, 24))[0]
st.bar_chart(hist_values)

st.write('## Locations')

hour_to_filter = st.slider('hour', 0, 23, 17)
data.rename(lambda x: x.lower(), axis='columns', inplace=True)
filtered_data = data[data['date/time'].dt.hour == hour_to_filter]

st.write('## Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)