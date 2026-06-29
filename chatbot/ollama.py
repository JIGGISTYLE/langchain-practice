from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama  # for ollama models

import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

# env vaiable call
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["GEMINI_API_KEY"]=os.getenv("GEMINI_API_KEY")
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")

#langchain_tracing
os.environ["LANGCHAIN_TRACING_V2"]="true"

#creating chatbot

promt=ChatPromptTemplate.from_messages(
    [
        ("system", " you are a helpul assistent. please provide solutions to the users querry"),
        ("user","question :{question}")
    ]
)

# streamlit
st.title("Langchain  demo with gemini api ")
input_text=st.text_input("search the topic you want")

# gemini ai llm call
llm = Ollama(model=" qwen2.5-coder:3b")   # change the ollama model 
output_parser=StrOutputParser()

#chain
chain=promt|llm|output_parser

if input_text:
    st.write(chain.invoke({"question":input_text}))