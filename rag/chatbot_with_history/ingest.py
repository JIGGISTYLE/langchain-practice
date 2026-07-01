# pyrefly: ignore [missing-import]
from dotenv import load_dotenv # for variable calling
import os 

# pyrefly: ignore [missing-import]
from langchain_community.document_loaders import PyPDFLoader # for loadig pdf

# pyrefly: ignore [missing-import]
from langchain_text_splitters import RecursiveCharacterTextSplitter # for splitting

# pyrefly: ignore [missing-import]
from langchain_ollama import OllamaEmbeddings # for embedding

# pyrefly: ignore [missing-import]
from langchain_chroma import Chroma # for vector database 
# pyrefly: ignore [missing-import]
import chromadb

load_dotenv()
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")
os.environ["LANGCHAIN_TRACING_V2"]="true"

#loader
loader=PyPDFLoader("documents/attention.pdf")
docs=loader.load() # 11 pages
#spliter
text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
chunks=text_splitter.split_documents(docs)
# embedding
embedding=OllamaEmbeddings(model="nomic-embed-text")

# vector db 
chroma_client = chromadb.HttpClient(host="localhost",port=8000)
db=Chroma(client=chroma_client,
        collection_name="attention_paper",
        embedding_function=embedding )
db.add_documents(chunks)



#for querry and result or use frontend

# query = "What is scaled dot-product attention?"
# results = db.similarity_search(query, k=3)

# print(results[0].page_content)
# print("Total vectors in collection:", db._collection.count())
#print("Total vectors in collection:", db._collection.count())

