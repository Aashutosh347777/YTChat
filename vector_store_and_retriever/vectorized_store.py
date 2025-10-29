import os
import shutil
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from loader_and_splitter import splitter

embedder = HuggingFaceEmbeddings(
    model_name = "all-MiniLM-L6-v2"
)
ROOT_DIRECTORY = "./chroma_transcript_store"
os.makedirs(ROOT_DIRECTORY,exist_ok=True)


# vector store
def vector_store(id):
    # giving a unique collection name 
    collection_name = "transcript"
    PERSIST_DIRECTORY = os.path.join(ROOT_DIRECTORY,id)

    # if the path exists we fetch the chroma client
    if os.path.exists(PERSIST_DIRECTORY):
        chroma_client = Chroma(
            collection_name= collection_name,
            embedding_function= embedder,
            persist_directory=PERSIST_DIRECTORY
        )

    else:
        transcript_doc = splitter.split_transcript_txt(id)

        # since the db is empty we reinstialize with from_documents.
        chroma_client = Chroma.from_documents(
            transcript_doc,
            embedding= embedder,
            collection_name=collection_name,
            persist_directory=PERSIST_DIRECTORY
        )
        
    return chroma_client
