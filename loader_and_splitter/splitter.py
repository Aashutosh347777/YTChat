from .loader import load_transcript
from langchain_text_splitters import RecursiveCharacterTextSplitter
import asyncio

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 0
)

def split_transcript_txt(id):
    text = asyncio.run(load_transcript(id))
    splitted_txt = splitter.create_documents([text['txt']]) # we pass the text as list so that we can correctly use the create_document method

    return splitted_txt

# output = split_transcript_txt("Z1GnEgCcCWE")

# print(type(output))
# print(type(output[3]),output[3].metadata,output[3].page_content)