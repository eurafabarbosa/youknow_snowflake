import pandas as pd
import numpy as np
import streamlit as st
import pinecone
from streamlit_player import st_player
from sentence_transformers import SentenceTransformer

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

############
# Pinecone #
############
pinecone.init(
    api_key=st.secrets["pinecone_api_key"],  # app.pinecone.io
    environment=t.secrets["pinecone_api_key_environment"]
)
index = pinecone.Index(st.secrets["pinecone_index_id"])

#############
# Embedding #
#############
model = SentenceTransformer("multi-qa-mpnet-base-dot-v1")


cs = conn.cursor()






st.title("YouKnow_Snow: The place for all your Snowflake Questions :snowflake:")

st.title(':tv: Videos')

cs.execute('SELECT Distinct AUTHOR FROM VIDEOS')
snowflake_channels = cs.fetch_pandas_all()
filter = st.selectbox(
    'Select Snowflake Channel',
    (snowflake_channels))

cs.execute(f"SELECT * FROM  VIDEOS WHERE AUTHOR LIKE '{filter}' order by PUB_DATE_MS DESC LIMIT 3")
snow_df = cs.fetch_pandas_all()
st.write(snow_df)

query = st.text_input('Ask a question about Snowflake', '', key="vid_search")
st.write(query)
if query:
    st.write(query)
#    xq = model.encode(query).tolist()
#    response = index.query(xq, top_k=3, include_metadata=True)
#    start = response['matches'][0]['metadata']['start']
#    url = response['matches'][0]['metadata']['title']+'&t='+str(start)+'s'
#    st_player(url, key="question_player")
    #st.write(url)
#    st.write(response['matches'])


row1_col1, row1_col2, row1_col3= st.columns((3,3,3))

with row1_col1:
    st_player(snow_df.VID_URL.iloc[0], key="col1a_player")