import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

st.title('My Parents New Healthy Diner.')

st.header('Breakfast Menu')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
# Import fruit data
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt").set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])

#Filter dataframe with users choice
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
st.dataframe(fruits_to_show)

fruit_choice = st.text_input('What fruit would you like information about?')
st.write('The user entered ', fruit_choice)

st.header('Fruityvice Fruit Advice!')
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

# normalize json response
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# show data as a table
st.dataframe(fruityvice_normalized)

# Add a button to load the fruit
if st.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
  my_cur = my_cnx.cursor()
  my_cur.execute("SELECT * FROM fruit_load_list")
  my_data_rows = my_cur.fetchall()
  st.header("Fruit list:")
  st.dataframe(my_data_rows)
  
  fruit_add = st.text_input('What fruit would you like to add?')
  st.write('Thanks for adding: ', fruit_add)
  if fruit_add not in my_data_rows:
    my_cur.execute("INSERT INTO fruit_load_list VALUES ('" + fruit_add + "');")
