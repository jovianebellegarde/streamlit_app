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
st.stop()

# connect to snowflake
my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
st.header("The fruit load list contains:")
st.dataframe(my_data_rows)

add_fruit_choice = st.text_input('What fruit would you like to add?',
                                 'Jackfruit')
st.write(f'Thanks for adding {add_fruit_choice}')

# will not work correctly, but seeing what happens for now
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
