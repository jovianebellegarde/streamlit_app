import streamlit
import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

st.title('My Parents New Healthy Diner')
st.header('Breakfast Favorites')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com"
                         "/dabw/fruit_macros.txt")
fruit_list = fruit_list.set_index('Fruit')

# put a pick list so user can pick the fruit they want to include
fruits_selected = st.multiselect('Pick some fruits:', list(fruit_list.index),
                                 ['Avocado', 'Strawberries'])
fruits_to_show = fruit_list.loc[fruits_selected]

# display table
st.dataframe(fruits_to_show)


def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"
                                       + this_fruit_choice)
    # take the json version of the response and normalize it
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized


# new section to display fruityvice api response
st.header('Fruityvice Fruit Advice!')

try:
    fruit_choice = st.text_input('What fruit would you like '
                                 'information about?')
    if not fruit_choice:
        st.error('Please select a fruit to get information')
    else:
        fruity_vice_data = get_fruityvice_data(fruit_choice)
        st.dataframe(fruity_vice_data)

except URLError as e:
    st.error()

# don't run anything past here while debugging
#st.stop()


# Snowflake-related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute('select * from fruit_load_list')
        return my_cur.fetchall()


# add a button to load the fruit
if st.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    st.dataframe(my_data_rows)

