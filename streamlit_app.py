import streamlit 
import pandas 
import requests
import snowflake.connector
from urllib.error import URLError

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect('Pick some fruits: ',list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]


streamlit.dataframe(fruits_to_show)

streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('what fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('please select a fruit to get information.')
  else:
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    #take the json version of the response and normalize it
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    # output it the screen as a table
    streamlit.dataframe(fruityvice_normalized)

except URLError as e:
  streamlit.error()
  
#streamlit.write('the user entered', fruit_choice)


# fetch from snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

# add second text entry box
fruit_add = streamlit.text_input('what fruit would you like to add ?','jackfruit')
streamlit.write('Thanks for adding jackfruit')

my_cur.execute("insert into fruit_load_list values ('from streamlit')")

streamlit.stop()
