import pysqlite3
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import pandas as pd
import numpy as np
import random
import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.buy_me_a_coffee import button
import sqlite3
import sqlite_vec
from typing import List
import struct

from transformers import pipeline

from sentence_transformers import SentenceTransformer
from ragatouille import RAGPretrainedModel



st.set_page_config(
    page_title='YouKnowSnowflake',
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
    db = sqlite3.connect("Ressources/vec.db", check_same_thread=False)
    db.enable_load_extension(True)
    sqlite_vec.load(db)
    db.enable_load_extension(False)
    return db
#db = get_db()

@st.cache_resource
def get_qa_model():
  # Get embedding model
  qa_model = pipeline("question-answering")#, model="meta-llama/Llama-3.2-1B")
  #qa_model = pipeline("question-answering", model='bert-base-cased')#, model="distilbert/distilbert-base-cased-distilled-squad")
  return qa_model
qa_model = get_qa_model()


@st.cache_resource
def get_rerank_model():
  # Get embedding model
  rerank_model = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0")
  #qa_model = pipeline("question-answering", model='distilbert/distilbert-base-cased-distilled-squad')#, model="distilbert/distilbert-base-cased-distilled-squad")
  return rerank_model
rerank_model = get_rerank_model()



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
    db = get_db()
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

    if "show_animation" not in st.session_state:
      st.session_state.show_animation = True

    if st.session_state.show_animation:
      components.html(particles_js, height=400, width=1300, scrolling=True)
    

    intro()

    left, middle, right = st.columns(3)

    question = random.choice(example_questions)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if left.button(f"{'✨ '+question+ ' ✨'}", use_container_width=True):
        query=embedding_model.encode(([question]))[0]
        result = db.execute(
            """
            SELECT
                youtube.text
            FROM youtube_vec
            left join youtube on youtube.id = youtube_vec.id
            WHERE embeddings MATCH ?
            and k = 20
            ORDER BY distance
            """,
            [sqlite_vec.serialize_float32(question)],
        ).fetchall()

        context = " "
        for res in result:
            context += text[0]
        final_answer = qa_model(question = question, context = context)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": question})
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": final_answer['answer']})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(question)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with st.container(height=300):
                response = st.write(final_answer, result)
        # Add assistant response to chat history
        #st.session_state.messages.append({"role": "assistant", "content": response})
    
    if prompt := st.chat_input("Ask me anything about Snowflake features or updates!"):
      #with st.container(height=300):
      #if prompt := st.chat_input("Ask me anything"):
        # Initialize chat history

      # Display chat messages from history on app rerun
      for message in st.session_state.messages:
        with st.chat_message(message["role"]):
          #with st.container(height=300):
          st.markdown(message["content"])
        
          #st.session_state.show_animation = False
          #st.session_state.messages.append({"role": "user", "content": prompt})

      # Accept user input
      if prompt:
        question=prompt
        query=embedding_model.encode(([prompt]))[0]
        
        result = db.execute(
            """
            SELECT
                youtube.text
                youtube.url
            FROM youtube_vec
            left join youtube on youtube.id = youtube_vec.id
            WHERE embeddings MATCH ?
            and k = 20
            ORDER BY distance
            """,
            [sqlite_vec.serialize_float32(query)],
        ).fetchall()
        
        #context = " "
        #for text in result:
        #  context += text[0]
        #final_answer = qa_model(question = prompt, context = context)
        context = []
        for text in result:
            #print(text[0])
            text = text[0]
            context.append(text)
        context = list(filter(None, context))
        reranked_result = rerank_model.rerank(query=question, documents=context, k=3)
        reranked_context=" "
        for context in reranked_result:
            reranked_context += context['content']        
        final_answer = qa_model(question=prompt, context=reranked_context)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": final_answer['answer']})
        # Display user message in chat message container
        with st.chat_message("user"):
          st.markdown(prompt)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
          with st.container(height=300):
            response = st.write(final_answer, reranked_result)
            #st.session_state.messages.append({"role": "assistant", "content": response})


    with st.sidebar:
      st.header("This is YouKnow Snowflake! ✨")
      with st.expander(":information_source: About the app"):
        st.info(
            "- Version 0.1.  \n"
            "- Roadmap: Colbert Retriever  \n"
            "- Roadmap: LLM service  \n"
        )
      #if st.button("Watch the latest on Artificial Intelligence"):
      #  show_video("")

      with st.expander(":gear: System Prompt"):
        st.success(
            "- Blablabal"
        )
        text_area_container = st.empty()
        sys_prompt = text_area_container.text_area("Instruct your AI", key="text")
        sys_prompt_btn = st.button("Customize your AI", on_click=update_sys_prompt)
        if sys_prompt_btn:
           st.success(
            f"Updated system prompt: {sys_prompt}"
        )
      
      with st.expander(":brain: Session History"):
        with st.container(height=300):
          if prompt or question:
            history = st.session_state.messages
            st.write(history)
          #if prompt:
            #st.write(results[0].metadata)
            #st.write(results[0].page_content)
      
      st.write("create video page")

      button(username="baurpasj", floating=False, width=221)

      with st.expander(":studio_microphone: Podcast Sources"):
        st.info(
            "- Machine Learning Street Talk  \n"
            "- TBA.  \n"
        )
      with st.expander(":tv: Video Sources"):
        st.info(
            "- Youtube  \n"
            "- TBA.  \n"
        )
      with st.expander(":newspaper: Text Sources"):
        st.info(
            "- xxx  \n"
            "- xxx  \n"
        )




















if __name__ == "__main__":
    main()