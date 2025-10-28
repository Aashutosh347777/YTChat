import os
import shutil
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from loader_and_splitter import splitter

embedder = HuggingFaceEmbeddings(
    model_name = "all-MiniLM-L6-v2"
)

PERSIST_DIRECTORY = "./chroma_store"

# vector store
def vector_store(id):
    if os.path.exists(PERSIST_DIRECTORY):
        try:
            shutil.rmtree(PERSIST_DIRECTORY)
        except Exception as e:
            print("Exception:",e)
            return None
        
    transcript_doc = splitter.split_transcript_txt(id)
    vector_store = Chroma.from_documents(transcript_doc, embedding=embedder, persist_directory=PERSIST_DIRECTORY)
    return vector_store
