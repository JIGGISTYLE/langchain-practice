# pyrefly: ignore [missing-import]
import streamlit as st
# pyrefly: ignore [missing-import]
import chromadb

# pyrefly: ignore [missing-import]
from langchain_chroma import Chroma
# pyrefly: ignore [missing-import]
from langchain_ollama import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain

from frontend import frontend

st.set_page_config(
    page_title="Attention Is All You Need | Study Companion",
    page_icon="\U0001F9E0",
    layout="wide",
    initial_sidebar_state="expanded",
)

frontend()

@st.cache_resource
def load_rag_chain():
    embedding = OllamaEmbeddings(model="nomic-embed-text")

    chroma_client = chromadb.HttpClient(host="localhost", port=8000)

    db = Chroma(
        client=chroma_client,
        collection_name="attention_paper",
        embedding_function=embedding,
    )

    retriever = db.as_retriever(search_kwargs={"k": 4})

    prompt = ChatPromptTemplate.from_template("""
Answer the following question only based on the context.
If the answer is not in the context, say "I don't know."

Context:
{context}

Question:
{input}
""")

    llm = Ollama(model="qwen2.5-coder:3b")

    document_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, document_chain)

    return rag_chain


rag_chain = load_rag_chain()


if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi! I am Nugget, your AI assistant. Ask me anything from the Attention paper."
        }
    ]


_, right_col = st.columns([5, 1])

with right_col:
    with st.popover("💬 Help & Support", use_container_width=True):
        st.markdown("### 🤖 attention support")
        st.caption("RAG chatbot connected to ChromaDB")
        st.divider()

        chat_history_box = st.container(height=300)

        with chat_history_box:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

        prompt = st.chat_input("Ask from attention paper...")

        if prompt:
            st.session_state.messages.append(
                {"role": "user", "content": prompt}
            )

            with st.spinner("Searching ChromaDB..."):
                result = rag_chain.invoke({"input": prompt})
                answer = result["answer"]

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

            st.rerun()