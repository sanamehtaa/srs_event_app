import streamlit as st
import openai
from openai import OpenAI
import time

# Page configuration
st.set_page_config(
    page_title="OpenAI Assistant Chat",
    page_icon="🤖",
    layout="wide"
)

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
ASSISTANT_ID = st.secrets["ASSISTANT_ID"]

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
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
st.title("🤖 OpenAI Assistant Chat")
st.markdown("---")

# Chat display area
chat_container = st.container()

with chat_container:
    # Display conversation history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Input area
with st.container():
    st.markdown("---")
    
    # Message input
    user_input = st.chat_input("Type your message here...")
    
    if user_input:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Get assistant response
        with st.chat_message("assistant"):
            with st.spinner("Assistant is thinking..."):
                response = send_message(user_input)
                
                if response:
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                else:
                    st.error("Failed to get response from assistant")

# Sidebar with controls
with st.sidebar:
    st.header("Controls")
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.thread_id = None
        st.rerun()
    
    st.markdown("---")
    st.markdown("**Instructions:**")
    st.markdown("1. Type your message in the input box")
    st.markdown("2. Press Enter or click Send")
    st.markdown("3. Wait for the assistant's response")
    st.markdown("4. Use 'Clear Chat' to start a new conversation") 