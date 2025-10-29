from .vectorized_store import vector_store
from langchain_classic.retrievers import MultiQueryRetriever
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

# creating retriever object
def retriever_functionality(id):
    vector_store_obj = vector_store(id)
    retriever = vector_store_obj.as_retriever(
        search_type = "mmr",
        search_kwargs = {
            "k":3,
            "fetch_k" : 10,
            "lambda_mult":0.5
        },
    ) #by default uses similarity for the search


    llm = ChatGoogleGenerativeAI(
        model = "gemini-2.5-flash-lite",
        temperature=0 # for consistent
    )

    mqr = MultiQueryRetriever.from_llm(
        retriever=retriever,
        llm=llm
    )

    return mqr

# output = retriever_functionality("Z1GnEgCcCWE")
# print(output.invoke("how was the journey to join forces?"))