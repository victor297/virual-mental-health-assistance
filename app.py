import streamlit as st
from guessing import main as guessing_game  # Import your custom guessing game
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set up Google Generative AI
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_API_KEY")

def get_gemini_response(user_message):
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    response = model.predict(user_message)
    return response

# Streamlit app layout
import random

st.subheader("Welcome to the Virtual Assistant for Mental Wellness!")

# Tabs for games and chatbot
tab1, tab2 = st.tabs(["Virtual Therapist", "Number Guessing Game"])

with tab1:
    st.header("Mental Therapist")
    
    # Input form for user message
    with st.form(key="chat_form"):
        user_message = st.text_input("Your message:", "")
        user_message_ai_input = "I need assistance for mental wellness. Help me, you will be my therapist, so here is my question: " + user_message
        submit_button = st.form_submit_button(label="Send")
        clear_button = st.form_submit_button(label="Clear Chat")

    # Display the chat log
    if "chat_log" not in st.session_state:
        st.session_state["chat_log"] = []

    # Handle form submissions
    if submit_button and user_message:
        response = get_gemini_response(user_message_ai_input)
        st.session_state["chat_log"].append(f"You: {user_message}")
        st.session_state["chat_log"].append(f"Therapist: {response}")
    
    if clear_button:
        st.session_state["chat_log"] = []

    # Display the chat log
    for chat in st.session_state["chat_log"]:
        st.write(chat)

with tab2:
    guessing_game()  
