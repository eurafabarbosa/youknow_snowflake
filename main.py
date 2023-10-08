import pandas as pd
import numpy as np
import streamlit as st
import pinecone
from streamlit_player import st_player
#from sentence_transformers import SentenceTransformer

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
    client_session_keep_alive=True)

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



# HANDLERS

def on_api_key_change():
	api_key = ss.get('api_key') or os.getenv('OPENAI_KEY')
	model.use_key(api_key) # TODO: empty api_key
	#
	if 'data_dict' not in ss: ss['data_dict'] = {} # used only with DictStorage
	ss['storage'] = storage.get_storage(api_key, data_dict=ss['data_dict'])
	ss['cache'] = cache.get_cache()
	ss['user'] = ss['storage'].folder # TODO: refactor user 'calculation' from get_storage
	model.set_user(ss['user'])
	ss['feedback'] = feedback.get_feedback_adapter(ss['user'])
	ss['feedback_score'] = ss['feedback'].get_score()
	#
	ss['debug']['storage.folder'] = ss['storage'].folder
	ss['debug']['storage.class'] = ss['storage'].__class__.__name__


# LAYOUT

# sidebar
with st.sidebar:
    st.write('## Enter your OpenAI API key')
    st.text_input('OpenAI API key', type='password', key='api_key', on_change=on_api_key_change, label_visibility="collapsed")



# page

st.title("YouKnow_Snow")
st.header("The place to answer all your Snowflake Questions :snowflake:")

st.title(':tv: Videos')

cs.execute("SELECT Distinct AUTHOR FROM VIDEOS WHERE AUTHOR LIKE 'Snowflake%' ")
snowflake_channels = cs.fetch_pandas_all()
filter = st.selectbox(
    'Select Snowflake Channel',
    (snowflake_channels))

cs.execute(f"SELECT * FROM  VIDEOS WHERE AUTHOR LIKE '{filter}' order by PUB_DATE_MS DESC LIMIT 3")
snow_df = cs.fetch_pandas_all()

query = st.text_input('Ask a question about Snowflake', '', key="vid_search")
if query:
    #xq = model.encode(query).tolist()
    xq = None
    response = index.query(xq, top_k=3, include_metadata=True)
    start = response['matches'][0]['metadata']['start']
    url = response['matches'][0]['metadata']['title']+'&t='+str(start)+'s'
    st_player(url, key="question_player")
#    st.write(url)
#    st.write(response['matches'])


st.header('Newest Videos')

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
