import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='NYC Peak Load Predictions',
    page_icon=':high_voltage:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def get_model_data():
    """Grab GDP data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/streamlit_data.csv'
    df = pd.read_csv(DATA_FILENAME)

    MIN_YEAR = 1960
    MAX_YEAR = 2022

    # The data above has columns like:
    # - Country Name
    # - Country Code
    # - [Stuff I don't care about]
    # - GDP for 1960
    # - GDP for 1961
    # - GDP for 1962
    # - ...
    # - GDP for 2022
    #
    # ...but I want this instead:
    # - Country Name
    # - Country Code
    # - Year
    # - GDP
    #
    # So let's pivot all those year-columns into two: Year and GDP

    # Convert years from string to integers
    df['year'] = pd.to_numeric(df['year'])
    df['date'] = pd.to_datetime(df['date'])

    df = df[['date', 'load', 'load_predict']].melt(id_vars=['date'])

    return df

df = get_model_data()

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :zap: NYC Peak Load

Brown model predictions from the [NYC Peak Load](https://github.com/jcaramichaellehigh/nyc-power) project. 
'''

# Add some spacing
''
''

min_value = df['date'].min()
max_value = df['date'].max()

#from_date, to_date = st.slider(
#    'Which years are you interested in?',
#    min_value=min_value,
#    max_value=max_value,
#    value=[min_value, max_value])
from_date, to_date = st.slider(
    "Select range",
    value=(pd.to_datetime(df['date'].min()).to_pydatetime(), pd.to_datetime(df['date'].max()).to_pydatetime())
)

''
''
''

# Filter the data
df_filter = df[df['date'].between(from_date, to_date)]

st.header('Observed vs. Predicted Load (MW)', divider='gray')

''

st.line_chart(
    df_filter,
    x='date',
    y='value',
    color='variable',
)

''
''
