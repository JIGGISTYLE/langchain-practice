
# pyrefly: ignore [missing-import]
from langchain_chroma import Chroma
# pyrefly: ignore [missing-import]
import chromadb
# pyrefly: ignore [missing-import]
from langchain_ollama import OllamaEmbeddings # for embedding
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain

from fastapi import FastAPI , HTTPException

from database import insert_message,get_history
# reconnect the vector databse 
embedding = OllamaEmbeddings(model="nomic-embed-text")
chroma_client = chromadb.HttpClient(host="localhost", port=8000)
db = Chroma(
    client=chroma_client,
    collection_name="attention_paper",
    embedding_function=embedding,
)
# retriever
retriever=db.as_retriever(search_kwargs={"k":4})
#promt
promt = ChatPromptTemplate.from_template("""
        answer the following question only based on the following context.
        if the answer isn't in the context , say you dont know.

        context:{context}

        question:{input}
""")
#llm
llm=Ollama(model="qwen2.5-coder:3b")

# chain : retriever+promt+llm
document_chain=create_stuff_documents_chain(llm,promt)
rag_chain=create_retrieval_chain(retriever,document_chain)


app=FastAPI()

@app.get("/")
def welcome():
    return {"message":"welcome"}
@app.post("/ask")
def ask(query):
    try:
        result=rag_chain.invoke({"input":query})
        insert_message(query,result["answer"])
        return {"answer":result["answer"]}
    except Exception as e:
        raise HTTPException(detail=str(e))


