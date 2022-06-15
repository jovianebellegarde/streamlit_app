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


# creating a function
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get(
        "https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized


# new section to display fruityvice api response
st.header('Fruityvice Fruit Advice!')
try:
    fruit_choice = st.text_input('What fruit would you like information about?')
    if not fruit_choice:
        st.error('Please select a fruit to get information.')
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        st.dataframe(back_from_function)
except URLError as e:
    st.error()


st.write(f'The user entered {fruit_choice}')

# don't run anything past here while we troubleshoot
st.stop()

# connector
my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
st.header("The fruit load list contains:")
st.dataframe(my_data_rows)


add_fruit = st.text_input('What fruit would you like to add?')
st.write(f'Thanks for adding {add_fruit}')

# this will not work correctly, but just go with it for now
my_cur.execute("insert into fruit_load_list values ('from streamlit')")