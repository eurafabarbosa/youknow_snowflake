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


st.set_page_config(
    page_title='YouKnowSnow',
    page_icon=':arrow_forward:',
    layout='wide',
    menu_items={
    'Get Help': 'https://www.google.com/',
    'Report a bug': 'https://www.google.com/',
    'About': 'Streamlit App to find answers about the Snowflake Data Cloud'

    },
)



def serialize_f32(vector: List[float]) -> bytes:
    """serializes a list of floats into a compact "raw bytes" format"""
    return struct.pack("%sf" % len(vector), *vector)


db = sqlite3.connect("Ressources/vec.db")
db.enable_load_extension(True)
sqlite_vec.load(db)
db.enable_load_extension(False)

with db:
    result = db.execute("SELECT id, text FROM youtube LIMIT 10").fetchall()
result

st.header('testing')
st.write(result)