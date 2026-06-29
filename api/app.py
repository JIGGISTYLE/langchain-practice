#backend


from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langserve import add_routes # adds specfic route for the chain "/endpoint"

import uvicorn
import os
from langchain_community.llms import Ollama  # qwen2.5-coder:3b
from dotenv import load_dotenv

load_dotenv()
# load env variable
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["GEMINI_API_KEY"]=os.getenv("GEMINI_API_KEY")
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")

# tracing
os.environ["LANGCHAIN_TRACING_V2"]="true"

# promts
gemini_prompt=ChatPromptTemplate.from_template("write essay on {topic} in 100 words")
ollama_prompt=ChatPromptTemplate.from_template("write song on {topic} in 100 words")

# llm call
gemini= ChatGoogleGenerativeAI(model="gemini-2.5-flash")
ollama=Ollama(model="qwen2.5-coder:3b")

# fast_api

app=FastAPI()

# adding diffrent routes
add_routes(
    app,
    gemini_prompt|gemini,
    path="/essay"
)

add_routes(
    app,
    ollama_prompt|ollama,
    path="/song"
)
