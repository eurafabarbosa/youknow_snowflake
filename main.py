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

ss = st.session_state


# Create a Snowflake connection function
conn = snowflake.connector.connect(
    account=st.secrets["account"],
    role=st.secrets["role"],
    warehouse=st.secrets["warehouse"],
    database=st.secrets["database"],
    schema=st.secrets["schema"],
    user=st.secrets["user"],
    password=st.secrets["password"],
    #client_session_keep_alive=True
    )

@st.cache_resource
def load_models():
    model = SentenceTransformer("multi-qa-mpnet-base-dot-v1")
    return model
model = load_models()
     

############
# Pinecone #
############
pinecone.init(
    api_key=st.secrets["pinecone_api_key"],  # app.pinecone.io
    environment=st.secrets["pinecone_api_key_environment"]
)
index = pinecone.Index(st.secrets["pinecone_index_id"])

#############
# Embedding #
#############
#model = SentenceTransformer("multi-qa-mpnet-base-dot-v1")


cs = conn.cursor()



# LAYOUT

# sidebar
with st.sidebar:
    st.title('Settings')
    configuration = st.radio(
    "Do you want Co-pilot to help you answer your questions in more detail?",
    ["***No***", "***Yes***"],
    captions = ["Semantic Search.", "Co-pilot response"])

    if configuration == '***No***':
        st.write('You selected No.')
    else:
        st.write("You Need to wait a little bit longer for this feature. It will be available in the upcoming release.")



# page

st.title("YouKnow_Snow")
st.header("The place to answer all your Snowflake Questions :snowflake:")

st.title(':tv: Videos')

rowa_cola, row1_colb, row1_colc = st.columns((3,3,3))

query = st.text_input('Ask a question about Snowflake', '', key="vid_search")
if query:
    xq = model.encode(query).tolist()
    response = index.query(xq, top_k=3, include_metadata=True)
    start = response['matches'][0]['metadata']['start']
    url = response['matches'][0]['metadata']['title']+'&t='+str(start)+'s'
    st_player(url, key="question_player")
#    st.write(url)
#    st.write(response['matches'])
    st.subheader('More relevant videos')
    with rowa_cola:
            st_player(response['matches'][1]['metadata']['url'], key="rowa_cola_player")
        #st.write(response['matches'][0]['metadata'], "score: ", response['matches'][0]['score'])
            expander = st.expander(":robot_face: See summary")
    with rowa_colb:
            st_player(response['matches'][2]['metadata']['url'], key="rowa_colb_player")
        #st.write(response['matches'][0]['metadata'], "score: ", response['matches'][0]['score'])
            expander = st.expander(":robot_face: See summary")
    with rowa_colc:
            st_player(response['matches'][3]['metadata']['url'], key="rowa_colc_player")
        #st.write(response['matches'][0]['metadata'], "score: ", response['matches'][0]['score'])
            expander = st.expander(":robot_face: See summary")


st.title('Latest Snowflake Videos')

cs.execute("SELECT Distinct AUTHOR FROM VIDEOS WHERE AUTHOR LIKE 'Snowflake%' ")
snowflake_channels = cs.fetch_pandas_all()
filter = st.selectbox(
    'Select Snowflake Channel',
    (snowflake_channels))
cs.execute(f"SELECT * FROM  VIDEOS WHERE AUTHOR LIKE '{filter}' order by PUB_DATE_MS DESC LIMIT 3")
snow_df = cs.fetch_pandas_all()

row1_col1, row1_col2, row1_col3= st.columns((3,3,3))

with row1_col1:
    st_player(snow_df.VID_URL.iloc[0], key="col1a_player")
    expander = st.expander(":robot_face: See summary")
    expander.write(
        snow_df.SUMMARY.iloc[0]
    )

with row1_col2:
    st_player(snow_df.VID_URL.iloc[1], key="col2a_player")
    expander = st.expander(":robot_face: See summary")
    expander.write(
        snow_df.SUMMARY.iloc[1]
    )

with row1_col3:
    st_player(snow_df.VID_URL.iloc[2], key="col3a_player")
    expander = st.expander(":robot_face: See summary")
    expander.write(
        snow_df.SUMMARY.iloc[2]
    )
