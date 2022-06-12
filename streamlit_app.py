import streamlit as st
import pandas as pd

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

# filter table based on fruits the user will choose
st.multiselect('Pick some fruits:', list(fruit_list.index), ['Avocado', 'Strawberries'])

# display table
st.dataframe(fruit_list)
