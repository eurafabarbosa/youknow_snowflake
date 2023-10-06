import pandas as pd
import numpy as np
import streamlit as st
#import pinecone

from snowflake.snowpark import Session


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
   "database": st.secrets["database"],
   "schema": st.secrets["schema"],
   "warehouse": st.secrets["warehouse"],
   "CLIENT_SESSION_KEEP_ALIVE": st.secrets["CLIENT_SESSION_KEEP_ALIVE"]
}

#session = Session.builder.configs(snowflake_conn).create()


st.title("YouKnow_X: Your daily digest :hamburger:")


