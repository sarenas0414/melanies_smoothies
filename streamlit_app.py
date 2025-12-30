# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(f" :cup_with_straw: Customize Your Smoothie!")

import streamlit as st

name_on_order = st.text_input('Name on Smoothie')
st.write('The name of Smoothie will be:', name_on_order)


st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Chosse up to 5 ingredients', my_dataframe, max_selections=5)


if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string=''

    for fuit_chosen in ingredients_list:
        ingredients_string +=fuit_chosen +' '
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    time_to_insert = st.button('Sumit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
