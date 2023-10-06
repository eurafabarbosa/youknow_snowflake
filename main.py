import pandas as pd
import numpy as np
import streamlit as st
#import pinecone
from streamlit_player import st_player

#from snowflake.snowpark import Session
import snowflake.connector


st.set_page_config(
    page_title='YouKnow_X',
    page_icon=':arrow_forward:',
    layout='wide',
    menu_items={
    'Get Help': 'https://www.google.com/',
    'Report a bug': 'https://www.google.com/',
    'About': 'Streamlit Podcast App'

    },
)


snowflake_conn = {
  "account": st.secrets["account"],
  "user": st.secrets["user"],
  "password": st.secrets["password"],
  "role": st.secrets["role"],
  "warehouse": st.secrets["warehouse"],
  "database": st.secrets["database"],
  "schema": st.secrets["schema"]
}


# Create a Snowflake connection function
conn = snowflake.connector.connect(
    account=st.secrets["account"],
    role=st.secrets["role"],
    warehouse=st.secrets["warehouse"],
    database=st.secrets["database"],
    schema=st.secrets["schema"],
    user=st.secrets["user"],
    password=st.secrets["password"],
    client_session_keep_alive=True)

cs = conn.cursor()

#session = Session.builder.configs(snowflake_conn).create()

sql = 'SELECT * FROM VIDEOS LIMIT 3'
cs.execute(sql)
df = cs.fetch_pandas_all()

#st.write(df)

#snow_df = session.sql(f"SELECT * FROM  VIDEOS WHERE AUTHOR LIKE '{filter}' order by PUB_DATE_MS DESC LIMIT 3").collect()

st.title("YouKnow_X: Your daily digest :hamburger:")


st.title(':tv: Videos')

snowflake_channels = cs.execute('SELECT Distinct AUTHOR FROM VIDEOS')
#snowflake_channels = session.sql(f"SELECT Distinct AUTHOR FROM VIDEOS").collect()
option = st.selectbox(
    'Select Snowflake Channel',
    (snowflake_channels))

row1_col1, row1_col2, row1_col3= st.columns((3,3,3))

with row1_col1:
    st_player(df.VID_URL.iloc[0], key="col1a_player")