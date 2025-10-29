from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough
from langchain_core.messages import HumanMessage,AIMessage,BaseMessage
from vector_store_and_retriever import retriever
from dotenv import load_dotenv
import asyncio

load_dotenv()

parser = StrOutputParser()

condense_q_system_prompt = """Given the following conversation and a follow-up question, rephrase the follow-up question to be a standalone question. 
Chat History: {chat_history}"""

condense_question_prompt = ChatPromptTemplate.from_messages([
    ("system", condense_q_system_prompt),
    ("human", "{question}"),
])

answer_system_prompt = """You are an excellent Youtube video summarizer. Use the context provided below to answer the user's question.
If the answer is not found in the context, clearly state that the information is not available in the provided sources.

Context:
{context}

Chat History: {chat_history}"""

answer_prompt = ChatPromptTemplate.from_messages([
    ("system", answer_system_prompt),
    ("human", "{question}"),
])

def get_rag_chain(id):
    llm_1 = "meta-llama/Llama-3.1-8B-Instruct"
    llm_2 = "HuggingFaceH4/zephyr-7b-beta"

    llm = HuggingFaceEndpoint(
        repo_id= llm_1,
        task= "text_generation",
        max_new_tokens=256,
        temperature=0.1 ,
        do_sample=False,
        streaming=True,
        timeout= 120
    )
    model = ChatHuggingFace(llm = llm)

    get_retriever = retriever.retriever_functionality(id)

    context_formatter = RunnableLambda(format_document)

    history_aware_chain = (condense_question_prompt| model| parser)

    def decide_rewriting(data):
        if data.get("chat_history") and len(data["chat_history"]) > 0:
            # we must convert list[BaseMessage] to string for the condense prompt
            return RunnableParallel(
                chat_history=lambda x: _format_history_to_string(x["chat_history"]),
                question=RunnablePassthrough()
            ) | history_aware_chain
        else:
            # if no history, pass the original question straight through
            return RunnablePassthrough.assign(question=lambda x: x["question"])
        
    final_history_aware_chain = RunnableParallel(
        question=decide_rewriting,
        original_question=lambda x: x["question"], 
        chat_history=RunnablePassthrough() # pass history along for the final prompt
    )

    retrieval_pipeline = get_retriever | context_formatter

    conversational_rag_chain = (
        final_history_aware_chain
        | RunnableParallel(
            context=RunnablePassthrough.assign(question=lambda x: x["question"]) | retrieval_pipeline,
            question=lambda x: x["original_question"],
            chat_history=lambda x: _format_history_to_string(x["chat_history"])
        )
        | answer_prompt
        | model
        | parser
    )

    return conversational_rag_chain, model


def format_document(docs):
    seen_content = set()
    unique_documents = []

    for doc in docs:
        # Use a clean version of the content to check for duplicates
        content_to_check = doc.page_content.strip()
        
        if content_to_check not in seen_content:
            seen_content.add(content_to_check)
            unique_documents.append(doc.page_content)
    return "\n\n---\n\n".join(unique_documents)

def format_chat_history(history_list: list[dict]) -> list[BaseMessage]:

    formatted_history = []
    for message in history_list:
        content = message["content"]
        if message["role"] == "user":
            formatted_history.append(HumanMessage(content=content))
        elif message["role"] == "assistant":
            formatted_history.append(AIMessage(content=content))
    return formatted_history

def _format_history_to_string(chat_history: list[BaseMessage]) -> str:
    formatted_string = ""
    for message in chat_history:
        if isinstance(message, HumanMessage):
            formatted_string += f"Human: {message.content}\n"
        elif isinstance(message, AIMessage):
            formatted_string += f"AI: {message.content}\n"
    return formatted_string

async def invoke_chain(rag_chain, chat_history_list,query):
    # using ainvoke instead of invoke and await it
    # await the asynchronous history call .aget_messages()
    formatted_history = format_chat_history(chat_history_list)

    response = await rag_chain.ainvoke({
        "question": query,
        "chat_history": formatted_history,
    })

    return response