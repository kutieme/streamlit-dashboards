import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')
@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state = st.text('Loading data...done! with cache')

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

import collections
hist_vals = collections.Counter(data[DATE_COLUMN].dt.hour)
counter_dict = dict(hist_vals)

bar = go.Bar(x = list(counter_dict.keys()), y = list(counter_dict.values()))

fig = go.Figure(data = bar)
chart = st.plotly_chart(fig)




hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)
