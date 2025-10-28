from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from loader_and_splitter import splitter

embedder = HuggingFaceEmbeddings(
    model_name = "all-MiniLM-L6-v2"
)
# vector store

def vector_store(id):
    transcript_doc = splitter.split_transcript_txt(id)
    vector_store = Chroma.from_documents(transcript_doc, embedding=embedder, persist_directory="./chroma_store")
    return vector_store


output = vector_store("Z1GnEgCcCWE")
print(output.get_by_ids([output.index_to_docstore_id[0]]))