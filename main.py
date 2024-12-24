import pysqlite3
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import pandas as pd
import numpy as np
import streamlit as st
import sqlite3
import sqlite_vec
from typing import List
import struct

from sentence_transformers import SentenceTransformer

embedding_model=SentenceTransformer("all-MiniLM-L6-v2")

st.set_page_config(
    page_title='YouKnowSnow',
    page_icon=':arrow_forward:',
    layout='wide',
    initial_sidebar_state="collapsed",
    menu_items={
    'Get Help': 'https://www.google.com/',
    'Report a bug': 'https://www.google.com/',
    'About': 'Streamlit App to find answers about the Snowflake Data Cloud'

    },
)



def serialize_f32(vector: List[float]) -> bytes:
    """serializes a list of floats into a compact "raw bytes" format"""
    return struct.pack("%sf" % len(vector), *vector)


@st.cache_data
def get_db():
    db = sqlite3.connect("Ressources/vec.db")
    db.enable_load_extension(True)
    sqlite_vec.load(db)
    db.enable_load_extension(False)
    return db
index = get_db()



example_questions = [
    "What is artificial intelligence?",
    "How does a transformer work?",
    "When will we reach general artificial intelligence?",
]

@st.cache_resource
def get_embedding_model():
  # Get embedding model
  hf_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
  return hf_embeddings
embeddings = get_embedding_model()





























st.header('simple test')
with db:
    result = db.execute("SELECT id, text FROM youtube LIMIT 10").fetchall()
st.write(result)


st.header('vector search test')

query=embedding_model.encode((["Since deploying the snowflake platform, how much has the performance improved"]))[0]

vec_result = db.execute(
    """
      SELECT
        youtube.id,
        youtube_vec.id,
        youtube.text
      FROM youtube_vec
      left join youtube on youtube.id = youtube_vec.id
      WHERE embeddings MATCH ?
      and k = 5
      ORDER BY distance
    """,
    [sqlite_vec.serialize_float32(query)],
).fetchall()

st.write(vec_result)


vec_result2 = db.execute(
    """
      SELECT
        *
      FROM youtube_vec
      LIMIT 2
    """).fetchall()

st.write(vec_result2)