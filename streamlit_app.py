import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

MY_CNX = snowflake.connector.connect(**st.secrets["snowflake"])


def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"
                                       + this_fruit_choice)
    # take the json version of the response and normalize it
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized


# Snowflake-related functions
def get_fruit_load_list():
    with MY_CNX.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()


# allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
    with MY_CNX.cursor() as my_cur:
        my_cur.execute(
            "insert into fruit_load_list values ('" + new_fruit + "')")
        return f'Thanks for adding {new_fruit}'


def main():
    st.title("My Parents New Healthy Diner")
    st.header("Breakfast Favorites")
    st.text("🥣 Omega 3 & Blueberry Oatmeal")
    st.text("🥗 Kale, Spinach & Rocket Smoothie")
    st.text("🐔 Hard-Boiled Free-Range Egg")
    st.text("🥑🍞 Avocado Toast")

    st.header("🍌🥭 Build Your Own Fruit Smoothie 🥝🍇")
    fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com"
                             "/dabw/fruit_macros.txt")
    fruit_list = fruit_list.set_index('Fruit')

    # put a pick list so user can pick the fruit they want to include
    fruits_selected = st.multiselect("Pick some fruits:",
                                     list(fruit_list.index),
                                     ["Avocado", "Strawberries"])
    fruits_to_show = fruit_list.loc[fruits_selected]

    # display table
    st.dataframe(fruits_to_show)

    try:
        fruit_choice = st.text_input("What fruit would you like "
                                     "information about?")
        if not fruit_choice:
            st.error("Please select a fruit to get information")
        else:
            fruity_vice_data = get_fruityvice_data(fruit_choice)
            st.dataframe(fruity_vice_data)

    except URLError:
        st.error()

    # new section to display fruityvice api response
    st.header("View Our Fruit List - Add Your Favorites!")

    # add a button to load the fruit
    if st.button("Get Fruit Load List"):
        my_cnx = MY_CNX
        my_data_rows = get_fruit_load_list()
        my_cnx.close()
        st.dataframe(my_data_rows)

    add_my_fruit = st.text_input("What fruit would you like to add?")
    if st.button("Add a Fruit to the List"):
        added_fruit = insert_row_snowflake(add_my_fruit)
        st.text(added_fruit)


main()
