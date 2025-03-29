import streamlit as st
import requests
from PIL import Image
import io
import os

# Streamlit App

st.title("VLM-Powered Document Understanding")
st.markdown("""
    Upload an image and provide a prompt to extract information and convert it to a structured format using a Vision Language Model.
""")

# --- Sidebar Configuration ---
st.sidebar.header("Configuration")
backend_url = st.sidebar.text_input("Backend URL", "http://localhost:8000")  # Default URL, user can change
# You could potentially add model selection to the sidebar if you wanted to extend the functionality

# --- File Upload ---
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# --- Text Prompt ---
text_prompt = st.text_area("Text Prompt", "Convert this page to docling.", height=100)

# --- Image Display ---
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# --- Process Button ---
if st.button("Process Image"):
    if uploaded_file is None:
        st.error("Please upload an image first.")
    else:
        # --- Prepare the Request ---
        files = {"files": (uploaded_file.name, uploaded_file, uploaded_file.type)}
        data = {"text_prompt": text_prompt}

        # --- Make the API Request ---
        try:
            with st.spinner("Processing image..."):  # Show spinner while processing
                response = requests.post(f"{backend_url}/process_image/", files=files, data=data)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

            result = response.json().get("result")

            if result:
                # --- Display the Result ---
                st.header("Result")
                st.markdown(result)

                # --- Download Button (Optional) ---
                st.download_button(
                  label="Download Markdown",
                  data=result,
                  file_name="output.md",
                  mime="text/markdown",
                )
            else:
                st.error("No result received from the backend.")

        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the backend: {e}")
        except Exception as e:
            st.error(f"An error occurred: {e}")

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
    "This application uses a Vision Language Model to process images based on a provided text prompt. "
    "It communicates with a backend server to perform the VLM processing.\n\n"
    "Based on docling-project"
)