import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Mom\'s New Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('ð¥£ Omega 3 & Blueberry Oatmeal')
streamlit.text('ð¥ Kale, Spinach & Rocket Smoothie')
streamlit.text('ð Hard-Boiled Free-Range Egg')
streamlit.text('ð¥ð Avocado Toast')
streamlit.header('ðð¥­Build Your Own Fruit Smoothie ð¥ð')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list =my_fruit_list.set_index('Fruit')
fruits_selected=streamlit.multiselect ("Pick Some Fruits :",list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show=my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)


def get_fruityvice_date(this_fruit_choice):
        fruityvice_response=requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
        fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
        return fruityvice_normalized

streamlit.header('Frutivice Fruit Advice')
try:
        fruit_choice=streamlit.text_input('What fruit would you like information about?')
        if not fruit_choice:
                streamlit.error("Please select a fruit to get information")
        else :
                back_from_function= get_fruityvice_data(fruit_choice)
                streamlit.dataframe(back_from_function)                
                
except URLError as e:
		streamlit.error()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST ")
my_data_row = my_cur.fetchall()
streamlit.header("The fruit load list containts:")
streamlit.dataframe(my_data_row)





add_my_fruit=streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('Thanks for adding',add_my_fruit)
my_cur.execute("insert into fruit_load_list values('from streamlit') ")

def insert_row_snowflake(new_fruit) :
	with my_cnx.cursor() as my_cur:
		my_cur.execute("insert into fruit_load_list values('from streamlit')")
		return "Thanks for adding " +new_fruit
if streamlit.button('Add a Fruit to the List' ):
	my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
	my_data_rows= get_fruit_load_list()
	my_cnx.close()	
	streamlit.dataframe(my_data_rows)
	
