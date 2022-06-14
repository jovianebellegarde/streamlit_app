import streamlit as st
import pandas as pd
import requests

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

# new section to display fruityvice api response
st.header('Fruityvice Fruit Advice!')

fruityvice_response = requests.get(
    "https://fruityvice.com/api/fruit/watermelon")
fruityvice_json_response = fruityvice_response.json()
st.text(fruityvice_json_response)  # just writes the data to the screen

# take the json version of the response and normalize it
fruityvice_normalized = pd.json_normalize(fruityvice_json_response)

# output the screen as a table
st.dataframe(fruityvice_normalized)
