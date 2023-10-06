import pandas as pd
import numpy as np
import streamlit as st
from snowflake.snowpark import Session
from resources.snow_config import snowflake_conn


# Everything is accessible via the st.secrets dict:
st.write("account name:", st.secrets["account"])



st.title("YouKnow_X: Your daily digest :hamburger:")


