# Yt Chat
A robust, architecturally sound Retrieval-Augmented Generation (RAG) system for performing contextual, multi-turn Q&A over any given YouTube video's transcript.

## Architecture Overview
Client -> Streamlit
Server -> FastAPI/Uvicorn

## Tech Stack
Frontend -> Streamlit (Interactive web interface for chat and URL input.)
Backend -> FastAPI, Uvicorn (High-performance asynchronous API service.)
Data Source -> youtube-transcript-api (Fetches raw video content for indexing.)
Embedding -> HuggingFaceEmbedings(Seamless integration with Runnables embdedding model ->(all-MiniLM-L6-v2))
Vector store -> Chroma (Storing Embeddings of the transcripts. Done locally inside a folder in this repo.)
RAG/ML -> LangChain (Orchestration of the RAG pipeline.)
LLM -> HuggingFace Endpoints (Used for both question condensation and final answer generation (e.g., Llama-3.1-8B-Instruct).)

## Setup
### Repo setup
cd your_directory
git clone https://github.com/Aashutosh347777/YTChat.git

### Environment setup
python -m venv venv
cd venv
Scripts\activate
cd ..
pip install -r requirements.txt

### Note
Add a .env file where you can store your API keys.

## Running the system
Open two terminals with venv activated
In one terminal execute:
uvicorn api:app --reload

In other termimal execute:
streamlit run main.py