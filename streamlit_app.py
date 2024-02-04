import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


def get_fruityvice_data(this_fruit_choice):
     fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
     fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
     return fruityvice_normalized  

streamlit.title('My Moms New Healthy Dinner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)


streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
     streamlit.error("Please select a fruit to get information")
  else:
     back_from_function = get_fruityvice_data(fruit_choice)
     streamlit.dataframe(back_from_function)
     streamlit.write('The user entered ', fruit_choice)

except URLError as e: 
  streamlit.error() 


my_cnx =  snowflake.connector.connectmy_cnx =  snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from  fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)


def insert_row_snowflake(new_fruit):
     with my_cnx.cursor() as my_cur:
          my_cur.execute(" insert into fruit_load_list values ('" + new_fruit + "')")
          return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?' )
if streamlit.button('Add A Fruit to the List'): 
     back_from_function = insert_row_snowflake(add_my_fruit)
     streamlit.text(back_from_function)


