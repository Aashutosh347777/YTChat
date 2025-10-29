from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import asyncio
import logging
from chat.chat import get_rag_chain, invoke_chain


# fastapi object
app = FastAPI(
    title="YouTube RAG Chain API",
    description="Serves the asynchronous RAG chain for the Streamlit front-end.",
)

# mimicking Streamlit's @st.cache_resource
RAG_CHAIN_CACHE: Dict[str, Any] = {}

# logging for better visibility in the terminal
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    video_id: str
    question: str
    chat_history: List[ChatMessage]


@app.on_event("startup")
async def startup_event():
    logger.info("FastAPI service started.")

async def get_cached_chain(video_id: str):
    if video_id not in RAG_CHAIN_CACHE:
        logger.info(f"RAG Chain not found in cache. Loading for video ID: {video_id}")
        try:
            rag_chain, _ = await asyncio.to_thread(get_rag_chain, video_id)
            RAG_CHAIN_CACHE[video_id] = rag_chain
            logger.info(f"Successfully cached RAG Chain for video ID: {video_id}")
        except Exception as e:
            logger.error(f"Failed to load RAG Chain for ID {video_id}: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Could not load RAG resources for video ID '{video_id}'. Error: {e}"
            )
    
    return RAG_CHAIN_CACHE[video_id]



@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    video_id = request.video_id
    
    # load the RAG chain
    rag_chain = await get_cached_chain(video_id)
    
    # extracting and format the history for the invoke_chain function
    # also convert Pydantic models back to standard list[dict] for invoke_chain
    raw_history_list = [
        {"role": msg.role, "content": msg.content} 
        for msg in request.chat_history
    ]
    
    #  RAG invocation function
    try:
        response = await invoke_chain(
            rag_chain=rag_chain,
            chat_history_list=raw_history_list,
            query=request.question
        )
        
        return {"answer": response}

    except Exception as e:
        logger.error(f"Error during RAG chain invocation: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error during response generation: {e}"
        )
