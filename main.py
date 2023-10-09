import pandas as pd
import numpy as np
import streamlit as st
import pinecone
import time
from streamlit_player import st_player
from sentence_transformers import SentenceTransformer
import openai

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
    captions = ["Semantic Search", "Co-pilot response"])

    if configuration == '***No***':
        pass
    
    else:
        #st.write("You Need to wait a little bit longer for this feature. It will be available in the upcoming release.")
        st.write('## 1. Enter your OpenAI API key')
        openai_key = st.text_input('OpenAI API key', type='password', key='api_key', label_visibility="collapsed")
        #if openai_key:
        #    st.write(openai_key)



# PAGE

st.title("YouKnow_Snow")
st.header("The place to answer all your Snowflake Questions :snowflake:")

st.title(':tv: Videos')
query = st.text_input('Ask a question about Snowflake', '', key="vid_search")
if configuration == '***No***':
    if query:
        xq = model.encode(query).tolist()
        response = index.query(xq, top_k=4, include_metadata=True)
        start = response['matches'][0]['metadata']['start']
        url = response['matches'][0]['metadata']['title']+'&t='+str(start)+'s'
        st_player(url, key="question_player")

        st.subheader('More relevant videos')
        rowa_cola, rowa_colb, rowa_colc = st.columns((3,3,3))
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

else:
    if openai_key:
        openai.api_key = openai_key
        if query:
            xq = model.encode(query).tolist()
            response = index.query(xq, top_k=4, include_metadata=True)
            context = response['matches'][0]['metadata']['text']+response['matches'][1]['metadata']['text']+response['matches'][2]['metadata']['text']+response['matches'][3]['metadata']['text']
            prompt = f"Q: Answer the following question {query} in the third person form, limit your answer to two sentences and base your answer on the following context: {context} Answer:"
            with st.spinner('Thinking...'):
                res = openai.Completion.create(
                    engine='text-davinci-003',
                    prompt=prompt,
                    temperature=0,
                    max_tokens=400,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0,
                    stop=None
                )
            st.success('Here is your answer!')
    #st.write(res['choices'][0]['text'].strip())
            t = st.empty()
            for i in range(len(res['choices'][0]['text'].strip()) + 1):
                t.markdown("## %s..." % res['choices'][0]['text'].strip()[0:i])
                t.markdown(res['choices'][0]['text'].strip()[0:i])
                time.sleep(0.02)
    
            start = response['matches'][0]['metadata']['start']
            url = response['matches'][0]['metadata']['title']+'&t='+str(start)+'s'
            st_player(url, key="question_player")

            st.subheader('More relevant videos')
            rowa_cola, rowa_colb, rowa_colc = st.columns((3,3,3))
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
cs.execute(f"SELECT * FROM  VIDEOS WHERE AUTHOR LIKE '{filter}' order by PUB_DATE_MS DESC LIMIT 6")
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


row2_col1, row2_col2, row2_col3= st.columns((3,3,3))

with row2_col1:
    st_player(snow_df.VID_URL.iloc[3], key="row2_col1_player")
    expander = st.expander(":robot_face: See summary")
    expander.write(
        snow_df.SUMMARY.iloc[3]
    )

with row2_col2:
    st_player(snow_df.VID_URL.iloc[4], key="row2_col2_player")
    expander = st.expander(":robot_face: See summary")
    expander.write(
        snow_df.SUMMARY.iloc[4]
    )

with row2_col3:
    st_player(snow_df.VID_URL.iloc[5], key="row2_col3_player")
    expander = st.expander(":robot_face: See summary")
    expander.write(
        snow_df.SUMMARY.iloc[5]
    )