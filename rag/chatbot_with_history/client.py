import streamlit as st
import requests
from database import get_history

BACKEND_URL="http://127.0.0.1:8001"

st.title("ask questions from attention paper")


messages = st.container(height=300)
query=st.chat_input("enter your question here")

if query:
    messages.chat_message("user").write(query)
    param={"query":query}

    try:
        response=requests.post(f"{BACKEND_URL}/ask",params=param)
        if response.status_code == 200:
            result = response.json()
            messages.chat_message("assistant").write(result["answer"])
        else:
            st.error(f"Backend error: {response.status_code} - {response.text}")

    except requests.exceptions.ConnectionError:
        st.error("backend connection error")

if st.button("history"):
    for i in get_history():
        dict={}
        dict[i[1]]=i[2]
        for j,k in dict.items():
            messages.chat_message("user").write(j)
            messages.chat_message("assistant").write(k)
