# front end

import streamlit as st
import requests

#helper functions
def gemini_output( gemini_input ):
    response=requests.post("http://localhost:8000/essay/invoke", json={"input":{"topic":gemini_input}}) #"/invoke" to execute
    return response.json()["output"]["content"]

def ollama_output( ollama_input ):
    response=requests.post("http://localhost:8000/song/invoke", json={"input":{"topic":ollama_input}})
    return response.json()["output"]
# streamlit
st.title(" langchain demo with fastapi")
gemini_input=st.text_input("on what topic you would like to write an essay on?")
ollama_input=st.text_input(" on what topic would you like a song on?")

if gemini_input:
    st.write(gemini_output(gemini_input))
if ollama_input:
    st.write(ollama_output(ollama_input))

