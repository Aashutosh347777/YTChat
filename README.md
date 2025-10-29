# 💬 Yt Chat

A robust, architecturally sound **Retrieval-Augmented Generation (RAG)** system for performing contextual, multi-turn Q&A over any given YouTube video's transcript.

---

## Architecture Overview

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Client** | Streamlit | Frontend Interface |
| **Server** | FastAPI / Uvicorn | Backend API Service |

---

## Tech Stack

This project utilizes the following technologies, orchestrating them via LangChain for the RAG pipeline:

* **Frontend**: **Streamlit** (Interactive web interface for chat and URL input.)
* **Backend**: **FastAPI**, **Uvicorn** (High-performance asynchronous API service.)
* **Data Source**: `youtube-transcript-api` (Fetches raw video transcripts for indexing.)
* **Vector Store**: **Chroma** (Stores embeddings of the transcripts locally.)
* **Embedding**: **HuggingFaceEmbeddings**
    * **Model**: `all-MiniLM-L6-v2` (Seamlessly integrated via LangChain Runnables.)
* **RAG/Orchestration**: **LangChain** (Orchestrates the entire RAG pipeline.)
* **LLM**: **HuggingFace Endpoints**
    * **Purpose**: Used for both question condensation and final answer generation.
    * **Example Model**: Llama-3.1-8B-Instruct.

---

##  Setup

### 1. Repo Setup

Clone the repository into your desired directory:

```bash
cd your_directory
git clone [https://github.com/Aashutosh347777/YTChat.git](https://github.com/Aashutosh347777/YTChat.git)
```

### Environment setup
```bash
python -m venv venv
cd venv
Scripts\activate
cd ..
pip install -r requirements.txt
```

### Note
Add a .env file where you can store your API keys.

## Running the system
Open two terminals with venv activated <br>
In one terminal execute: <br>
```bash
uvicorn api:app --reload
```

In other termimal execute:<br>
```bash
streamlit run main.py
```