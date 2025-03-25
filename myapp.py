import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="Gemini AI Chat",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better appearance
st.markdown("""
    <style>
        .stTextInput input {
            height: 60px;
            font-size: 16px;
        }
        .stButton button {
            width: 100%;
            height: 50px;
            font-size: 16px;
            background-color: #4CAF50;
            color: white;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        .response-area {
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 10px;
            margin-top: 20px;
        }
        .title {
            color: #4CAF50;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🤖 MY  AI Chat Assistant ")
st.markdown("Ask anything to the Gemini 2.0 Flash model and get instant responses!")

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Sidebar for API key input (or use environment variable)
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter your Gemini API Key:", type="password", 
                           value=os.getenv("GEMINI_API_KEY", ""))
    
    if api_key:
        genai.configure(api_key=api_key)
        st.success("API key configured!")
    else:
        st.warning("Please enter your API key to continue")
    
    st.markdown("---")
    st.markdown("**Note:** Your API key is not stored and is only used for the current session.")

# Main chat interface
if api_key:
    # Initialize the model
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # User input
    user_input = st.chat_input("Ask me anything...")
    
    if user_input:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Get AI response
        try:
            response = model.generate_content(user_input)
            
            # Add AI response to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": response.text})
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
else:
    st.info("Please enter your Gemini API key in the sidebar to start chatting.")