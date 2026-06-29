# pyrefly: ignore [missing-import]
from langchain_community.document_loaders import TextLoader

# pyrefly: ignore [missing-import]
from langchain_community.document_loaders import WebBaseLoader
# pyrefly: ignore [missing-import]
import bs4

# pyrefly: ignore [missing-import]
from langchain_community.document_loaders import PyPDFLoader

# pyrefly: ignore [missing-import]
from langchain_text_splitters import RecursiveCharacterTextSplitter

# pyrefly: ignore [missing-import]
from langchain_ollama import OllamaEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
# pyrefly: ignore [missing-import]
from langchain_community.vectorstores import FAISS


import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

load_dotenv()
# load env variable
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["GEMINI_API_KEY"]=os.getenv("GEMINI_API_KEY")
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")

# tracing
os.environ["LANGCHAIN_TRACING_V2"]="true"

os.environ["USER_AGENT"] = "Jitesh-RAG-App/1.0"

# for loading txt files
loader=TextLoader("file.txt", encoding="utf-8")
text_docs=loader.load()

# for loading web based ( fixed format )

loader=WebBaseLoader(web_paths=("https://jamesclear.com/great-speeches/the-danger-of-a-single-story-by-chimamanda-ngozi-adichie",),
                    bs_kwargs=dict(parse_only=bs4.SoupStrainer(
                        class_=("post-title", "post-content", "post-header")
                    )))

web_docs=loader.load()

# for reading pdf
loader=PyPDFLoader("attention.pdf")
pdf_docs=loader.load()


#split the docs into chunks
text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
chunk_documents=text_splitter.split_documents(pdf_docs)

# embedding
db_gemini=FAISS.from_documents(chunk_documents,GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001"))
db_ollama=FAISS.from_documents (chunk_documents, OllamaEmbeddings(model="nomic-embed-text"))

# vectore stores and similarity search

query="Recurrent neural networks, long short-term memory [12] and gated recurrent [7] neural network"
retrieved_result=db_gemini.similarity_search(query)
print(retrieved_result[0].page_content)