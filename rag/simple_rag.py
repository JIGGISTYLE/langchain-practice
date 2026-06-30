import warnings
warnings.filterwarnings("ignore")

# pyrefly: ignore [missing-import]
import bs4
# pyrefly: ignore [missing-import]
from langchain_community.document_loaders import PyPDFLoader
# pyrefly: ignore [missing-import]
from langchain_text_splitters import RecursiveCharacterTextSplitter
# pyrefly: ignore [missing-import]
from langchain_ollama import OllamaEmbeddings
# pyrefly: ignore [missing-import]
from langchain_google_genai import GoogleGenerativeAIEmbeddings
# pyrefly: ignore [missing-import]
from langchain_community.vectorstores import FAISS

import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "") 
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "")
os.environ["LANGCHAIN_TRACING_V2"] = "true"

# for reading pdf
loader = PyPDFLoader("attention.pdf")
pdf_docs = loader.load()

# split into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunk_documents = text_splitter.split_documents(pdf_docs)

# embeddings + vector stores
db_gemini = FAISS.from_documents(chunk_documents, GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001"))
db_ollama = FAISS.from_documents(chunk_documents, OllamaEmbeddings(model="nomic-embed-text"))

# similarity search
query = "The decoder is also composed of a stack of N = 6 identical layers. "
retrieved_result = db_gemini.similarity_search(query)
print(retrieved_result[0].page_content)