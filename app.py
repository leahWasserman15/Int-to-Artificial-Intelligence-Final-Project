import streamlit as st
from dataclasses import dataclass
import pytesseract
from PIL import Image
import io
import re
import cv2
import numpy as np
import OCR

from  OCR import *

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "Invoice Reader", "content": "Submit an invoice and I will read it."}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

USER = "user"
ASSISTANT = "Invoice Reader"

# Accept file uploads
uploaded_file = st.file_uploader("Upload an invoice", type=["pdf", "png", "jpg", "jpeg"])
if uploaded_file is not None:
    # Display uploaded file content
    file_content = uploaded_file.getvalue()
    st.session_state.messages.append({"role": USER, "content": f"Uploaded file: {uploaded_file.name}"})
    with st.chat_message(USER):
        st.markdown(f"Uploaded file: {uploaded_file.name}")

    # Preprocess and extract text from image or PDF
    try:
        if uploaded_file.type == "application/pdf":
            text = extract_text_from_pdf(file_content)
        else:
            text = extract_text_from_image(file_content)

        # Extract specific details
        details = extract_invoice_details(text)

        # Create and display assistant's response to extracted text
        assistant_response = (
            f"Extracted text from the uploaded file:\n\n{text}\n\n"
            f"**Extracted Details:**\n"
            f"**Invoice Number:** {details['Invoice Number']}\n"
            
            f"**Amount:** {details['Amount']}\n"
            f"**Invoice Date:** {details['Invoice Date']}\n"
            f"**Due Date:** {details['Due Date']}"
        )
        st.session_state.messages.append({"role": ASSISTANT, "content": assistant_response})
        with st.chat_message(ASSISTANT):
            st.markdown(assistant_response)
    except Exception as e:
        error_message = f"An error occurred while processing the file: {e}"
        st.session_state.messages.append({"role": ASSISTANT, "content": error_message})
        with st.chat_message(ASSISTANT):
            st.markdown(error_message)


#streamlit run C:/Users/leahw/PycharmProjects/Int-to-Artificial-Intelligence-Final-Project/app.py