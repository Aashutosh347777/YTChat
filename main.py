import streamlit as st
import re
import requests

API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Conversational RAG Chatbot")

def call_rag_api(video_id: str, chat_history: list, question: str):
    """Makes a synchronous request to the FastAPI chat endpoint."""
    
    # Format LangChain messages for API (assuming FastAPI accepts simple JSON list)
    # The API will expect the full history to maintain context
    api_history = [{"role": m["role"], "content": m["content"]} for m in chat_history]

    payload = {
        "video_id": video_id,
        "question": question,
        "chat_history": api_history
    }
    
    # Make the synchronous HTTP POST request
    response = requests.post(f"{API_BASE_URL}/chat", json=payload)
    
    # Check for success
    if response.status_code == 200:
        return response.json().get("answer")
    else:
        st.error(f"API Error ({response.status_code}): {response.text}")
        return None

def extract_video_id(url_or_id: str) -> str:
    if not url_or_id:
        return ""
    
    # full url 
    match_v = re.search(r'(?:v=|youtu\.be\/|embed\/)([a-zA-Z0-9_-]{11})', url_or_id)
    if match_v:
        return match_v.group(1)
    
    # id
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url_or_id):
        return url_or_id
    
    return "" 

# call back function
def reset_session_state():
    st.session_state.chain_loaded = False
    st.session_state.messages = []
    st.toast("New video loaded. Chat history cleared.", icon="🔄")


#streamlit ui and state management
st.title("Video RAG Chatbot 💬")

#input field for the video id
st.sidebar.header("Video Configuration")
video_input = st.sidebar.text_input(
    "Enter YouTube Video ID:",
    value="",
    key="video_id_input",
    on_change=reset_session_state #call the reset function on every change
)

selected_video_id = extract_video_id(video_input)

# initialize session states if they don't exist
if "video_id_set" not in st.session_state:
    st.session_state.video_id_set = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if selected_video_id:
    st.session_state.video_id_set = True
    st.sidebar.success(f"Video ID recognized: {selected_video_id}")
else:
    st.info("Please enter a valid YouTube link or 11-character Video ID in the sidebar to begin.")
    st.session_state.video_id_set = False
    st.stop()

# display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# user input
if prompt := st.chat_input("Ask a question about the video...", disabled=not st.session_state.video_id_set):
    
    # user message to display list
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching and generating response..."):
            try:
                # ivoking the chain
                response = call_rag_api(
                    video_id=selected_video_id,
                    chat_history=st.session_state.messages, # Pass the entire UI history list
                    question=prompt
                )
            except Exception as e:
                response = f"An error occurred during response generation: {e}"
            
            # display and update history
            if response:
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                 st.error("Failed to get response from the RAG service.")