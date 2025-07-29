# app.py

import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate

# --- Page Configuration ---
st.set_page_config(
    page_title="Enhanced Functional Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# --- UI Styling ---
st.markdown("""
<style>
    .stApp {
        background-color: #323d53;
    }
    .st-chat-message {
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    .st-chat-message-user {
        background-color: #dcf8c6;
    }
    .st-chat-message-assistant {
        background-color: #ffffff;
    }
    .st-sidebar .st-text-input > div > div > input,
    .st-sidebar .st-text-area > div > textarea {
        background-color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar for Configuration ---
with st.sidebar:
    st.header("🤖 Configuration")
    st.markdown("Configure your chatbot's settings.")

    # API Key Input
    groq_api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="Enter your Groq API Key here",
        help="Get your free API key from https://console.groq.com/keys"
    )

    # System Prompt / Persona Configuration
    st.markdown("### Chatbot Persona")
    default_persona = "You are a helpful and friendly assistant. You respond concisely and accurately."
    system_prompt = st.text_area(
        "System Prompt",
        value=default_persona,
        height=150,
        help="Define the personality and instructions for the chatbot."
    )

    # Conversation Memory Window
    st.markdown("### Conversation Memory")
    memory_window = st.slider(
        "Memory Window Size",
        min_value=0,
        max_value=20,
        value=10,
        help="Number of past messages to remember. Set to 0 to disable memory."
    )

    # Model Selection
    st.markdown("### LLM Model")
    model_name = st.selectbox(
        "Choose a model",
        ('gemma2-9b-it', 'llama3-70b-8192', 'llama3-8b-8192', 'mixtral-8x7b-32768'),
        index=0 # Default to gemma-7b-it
    )

# --- Main Application Logic ---
st.title("Enhanced Functional Chatbot")
st.markdown("Powered by LangChain, Gemma, and Groq for high-speed conversations.")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you today?"}]

# Initialize conversation chain in session state
if "conversation" not in st.session_state:
    st.session_state.conversation = None

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to generate streaming response
def stream_response(chain, user_input):
    """Yields the streaming response chunks from the conversation chain."""
    full_response = ""
    for chunk in chain.stream({"input": user_input}):
        if "response" in chunk:
            response_piece = chunk["response"]
            full_response += response_piece
            yield response_piece

# Handle user input
if user_input := st.chat_input("What would you like to ask?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Check for API Key
    if not groq_api_key:
        with st.chat_message("assistant"):
            st.warning("Please enter your Groq API Key in the sidebar to continue.")
        st.stop()
        
    # --- Conversation Chain Initialization ---
    # Create a new chain if it doesn't exist or if settings have changed
    if st.session_state.conversation is None:
        try:
            # Define the prompt template
            prompt = PromptTemplate(
                template=f"""
                {system_prompt}

                Current conversation:
                {{history}}

                Human: {{input}}
                Assistant:
                """,
                input_variables=["history", "input"]
            )

            # Initialize the ChatGroq model
            llm = ChatGroq(
                api_key=groq_api_key,
                model_name=model_name,
                temperature=0.7
            )

            # Initialize memory
            memory = ConversationBufferWindowMemory(k=memory_window, memory_key="history")
            
            # Create and store the conversation chain
            st.session_state.conversation = ConversationChain(
                llm=llm,
                prompt=prompt,
                memory=memory,
                verbose=False # Set to True to see chain activity in console
            )
        except Exception as e:
            st.error(f"Failed to initialize the chatbot. Error: {e}")
            st.stop()


    # Generate and display assistant's response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = st.write_stream(stream_response(st.session_state.conversation, user_input))

    # Add assistant's final response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
