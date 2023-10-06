import pandas as pd
import numpy as np
import streamlit as st
import pinecone

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

# Everything is accessible via the st.secrets dict:

st.title("YouKnow_X: Your daily digest :hamburger:")


