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


@st.cache_resource
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
  embedding_model=SentenceTransformer("all-MiniLM-L6-v2")
  return embedding_model
embedding_model = get_embedding_model()


@st.dialog("How to use ...", width=1920)
def show_video(item):
    video_url = "https://www.youtube.com/watch?v=_iETa2KDRuw"
    st.video(video_url, loop=False, autoplay=True, muted=True)
    st.audio("https://anchor.fm/s/1e4a0eac/podcast/play/93482713/https%3A%2F%2Fd3ctxlq1ktw2nl.cloudfront.net%2Fstaging%2F2024-9-24%2Fcd5c61f1-9788-f730-6d4b-135bda34ee73.mp3")

def intro():
    """Main Home page intro"""
    #st.header("**This is YouKnow AI!**")


def update_sys_prompt():
        st.session_state.text


def main():
    """Main function to run the Streamlit app."""
    #st.set_page_config(
        #page_title="Test to SQL Generator — by Ahmed Salim",
        #page_icon=Image.open("app/ui/static/favicon.ico"),
        #layout="wide",
        #initial_sidebar_state="collapsed"
    #)
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    particles_js = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Particles.js</title>
  <style>
  #particles-js {
    position: fixed;
    width: 100vw;
    height: 100vh;
    top: 0;
    left: 0;
    z-index: -1; /* Send the animation to the back */
  }
  .content {
    position: relative;
    z-index: 1;
    color: white;
  }
  
</style>
</head>
<body>
  <div id="particles-js"></div>
  <div class="content">
    <!-- Placeholder for Streamlit content -->
  </div>
  <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
  <script>
    particlesJS("particles-js", {
      "particles": {
        "number": {
          "value": 150,
          "density": {
            "enable": true,
            "value_area": 1500
          }
        },
        "color": {
          "value": "#ffffff"
        },
        "shape": {
          "type": "circle",
          "stroke": {
            "width": 0,
            "color": "#000000"
          },
          "polygon": {
            "nb_sides": 5
          },
          "image": {
            "src": "img/github.svg",
            "width": 100,
            "height": 100
          }
        },
        "opacity": {
          "value": 0.5,
          "random": false,
          "anim": {
            "enable": false,
            "speed": 1,
            "opacity_min": 0.2,
            "sync": false
          }
        },
        "size": {
          "value": 2,
          "random": true,
          "anim": {
            "enable": false,
            "speed": 40,
            "size_min": 0.1,
            "sync": false
          }
        },
        "line_linked": {
          "enable": true,
          "distance": 100,
          "color": "#ffffff",
          "opacity": 0.22,
          "width": 1
        },
        "move": {
          "enable": true,
          "speed": 0.2,
          "direction": "none",
          "random": false,
          "straight": false,
          "out_mode": "out",
          "bounce": true,
          "attract": {
            "enable": false,
            "rotateX": 600,
            "rotateY": 1200
          }
        }
      },
      "interactivity": {
        "detect_on": "canvas",
        "events": {
          "onhover": {
            "enable": true,
            "mode": "grab"
          },
          "onclick": {
            "enable": true,
            "mode": "repulse"
          },
          "resize": true
        },
        "modes": {
          "grab": {
            "distance": 100,
            "line_linked": {
              "opacity": 1
            }
          },
          "bubble": {
            "distance": 400,
            "size": 2,
            "duration": 2,
            "opacity": 0.5,
            "speed": 1
          },
          "repulse": {
            "distance": 200,
            "duration": 0.4
          },
          "push": {
            "particles_nb": 2
          },
          "remove": {
            "particles_nb": 3
          }
        }
      },
      "retina_detect": true
    });
  </script>
</body>
</html>
"""






















if __name__ == "__main__":
    main()


'''
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
'''