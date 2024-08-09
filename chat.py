import streamlit as st
from langchain_google_genai import  ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set up Google Generative AI
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_API_KEY")

# Function to send a message to Gemini and get a response

def get_gemini_response(user_message_ai_input):
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    response = model.predict(user_message_ai_input)
    return response


# Streamlit app layout
st.write("Enter your message to translate it 📖📕!")

# Input form for user message
with st.form(key="chat_form"):
    user_message = st.text_input("Your message:", "")
    user_message_ai_input= ""
    submit_button = st.form_submit_button(label="Send")

# Display the chat log
if "chat_log" not in st.session_state:
    st.session_state["chat_log"] = []

# Handle form submissions
if submit_button and user_message_ai_input:
    response = get_gemini_response(user_message_ai_input)
    st.session_state["chat_log"].append(f"You: {user_message}")
    st.session_state["chat_log"].append(f"Translated to: {response}")

# Display the chat log
for chat in st.session_state["chat_log"]:
    st.write(chat)
