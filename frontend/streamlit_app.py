import streamlit as st
import requests
from PIL import Image
import io
import os
import json
import time

# Streamlit App

st.title("VLM-Powered Chatbot")
st.markdown("""
    Interact with a Vision Language Model by sending images and text prompts!
""")

# --- Sidebar Configuration ---
st.sidebar.header("Configuration")
backend_url = st.sidebar.text_input("Backend URL", "http://localhost:8500")  # Default URL, user can change
# You could potentially add model selection to the sidebar if you wanted to extend the functionality

# --- Chat History ---
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

def display_chat_history():
    for message in st.session_state['chat_history']:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- Image Upload ---
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# --- Text Input ---
text_prompt = st.chat_input("Enter your prompt here...")

# --- Process User Input ---
if uploaded_file or text_prompt:
    user_message = {}
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.session_state['chat_history'].append({"role": "user", "content": f"Image: {uploaded_file.name}"})
        user_message["image"] = {"name": uploaded_file.name, "content": uploaded_file.getvalue(), "type": uploaded_file.type}
    if text_prompt:
        st.session_state['chat_history'].append({"role": "user", "content": text_prompt})
        user_message["text"] = text_prompt
        
    display_chat_history()

    # --- Make the API Request ---
    try:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            # Prepare the request data
            data = {"text_prompt": user_message.get("text", None)} # Only send text prompt if it exists
            files = {}

            if user_message.get("image"):
              files = {"files": (user_message["image"]["name"], user_message["image"]["content"], user_message["image"]["type"])}

            # Streaming API Call
            with requests.post(f"{backend_url}/stream_process_image/", files=files, data=data, stream=True) as response:
                response.raise_for_status()
                for chunk in response.iter_content(chunk_size=8192, decode_unicode=True):  # Adjust chunk_size as needed
                    if chunk:
                        full_response += chunk
                        message_placeholder.markdown(full_response + "▌")  # Display with typing indicator
                message_placeholder.markdown(full_response)  # Finalize the message

        st.session_state['chat_history'].append({"role": "assistant", "content": full_response})

    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the backend: {e}")
        st.session_state['chat_history'].append({"role": "assistant", "content": f"Error: {e}"})

    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.session_state['chat_history'].append({"role": "assistant", "content": f"Error: {e}"})

display_chat_history()

# --- Health Check (Optional) ---
if st.sidebar.checkbox("Check Backend Health"):
    try:
        response = requests.get(f"{backend_url}/health")
        response.raise_for_status()
        health_status = response.json()
        st.sidebar.success(f"Backend Health: {health_status}")
    except requests.exceptions.RequestException as e:
        st.sidebar.error(f"Backend Health Check Failed: {e}")

# --- About Section ---
st.sidebar.header("About")
st.sidebar.info(
    "This chatbot uses a Vision Language Model to process images and text based on your prompts. "
    "It communicates with a backend server to perform the VLM processing and streams the response."
)