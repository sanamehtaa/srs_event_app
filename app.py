import streamlit as st
import openai
from openai import OpenAI
import time
import os

def load_css():
    """Load external CSS file"""
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load custom CSS
load_css()

# Page configuration
st.set_page_config(
    page_title="Ask Lily",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

# Force light mode theme
st.markdown("""
<style>
    .stApp {
        background-color: white;
    }
    .stChatMessage {
        background-color: transparent;
    }
    .stChatMessage[data-testid="chatMessage"] {
        background-color: transparent;
    }
    .stChatInput {
        background-color: white;
    }
    /* Ensure assistant messages are visible */
    .stChatMessage:nth-child(even) .stChatMessageContent {
        background-color: #f8f9fa !important;
        color: #000000 !important;
        border: 1px solid #dee2e6 !important;
    }
    /* Ensure user messages are visible */
    .stChatMessage:nth-child(odd) .stChatMessageContent {
        background-color: #e3f2fd !important;
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize OpenAI client with error handling
try:
    # Try to get API key from environment variable first, then from Streamlit secrets
    api_key = os.getenv("OPENAI_API_KEY") or st.secrets["OPENAI_API_KEY"]
    assistant_id = os.getenv("ASSISTANT_ID") or st.secrets["ASSISTANT_ID"]
    
    client = OpenAI(api_key=api_key)
    ASSISTANT_ID = assistant_id
except (KeyError, TypeError):
    st.error("""
    ⚠️ **Configuration Error**
    
    Please configure your API keys using one of these methods:
    
    **Method 1: Environment Variables**
    Set these environment variables:
    ```
    OPENAI_API_KEY=your-openai-api-key-here
    ASSISTANT_ID=your-assistant-id-here
    ```
    
    **Method 2: Streamlit Secrets (Recommended for Streamlit Cloud)**
    1. Go to your app's dashboard
    2. Click "Settings" → "Secrets"
    3. Add your secrets:
    ```
    OPENAI_API_KEY = "your-openai-api-key-here"
    ASSISTANT_ID = "your-assistant-id-here"
    ```
    
    **Method 3: Local Development**
    Create a `.streamlit/secrets.toml` file with:
    ```
    OPENAI_API_KEY = "your-openai-api-key-here"
    ASSISTANT_ID = "your-assistant-id-here"
    ```
    """)
    st.stop()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "Hi! I am Lily, how can I help you with the SRS innovation summit?"
        }
    ]
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

def create_thread():
    """Create a new thread for the conversation"""
    thread = client.beta.threads.create()
    return thread.id

def send_message(message):
    """Send a message to the assistant and get response"""
    # Create thread if it doesn't exist
    if st.session_state.thread_id is None:
        st.session_state.thread_id = create_thread()
    
    # Add user message to thread
    client.beta.threads.messages.create(
        thread_id=st.session_state.thread_id,
        role="user",
        content=message
    )
    
    # Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=st.session_state.thread_id,
        assistant_id=ASSISTANT_ID
    )
    
    # Wait for the run to complete
    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=st.session_state.thread_id,
            run_id=run.id
        )
        if run_status.status == "completed":
            break
        elif run_status.status == "failed":
            st.error("Assistant run failed")
            return None
        time.sleep(0.5)
    
    # Get the assistant's response
    messages = client.beta.threads.messages.list(
        thread_id=st.session_state.thread_id
    )
    
    # Return the latest assistant message
    for msg in messages.data:
        if msg.role == "assistant":
            return msg.content[0].text.value
    return None

# App header
st.title("💬 Ask Lily")

# Chat display area
chat_container = st.container()

with chat_container:
    # Display conversation history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Input area
with st.container():
    # Message input
    user_input = st.chat_input("Message Lily...")
    
    if user_input:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Get assistant response
        with st.chat_message("assistant"):
            with st.spinner("AI is thinking..."):
                response = send_message(user_input)
                
                if response:
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                else:
                    st.error("Failed to get response from assistant")

 