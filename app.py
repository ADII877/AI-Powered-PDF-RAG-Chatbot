# Import Libraries

import streamlit as st
import os

from ingest import ingest_pdf
from query import ask_question


# Streamlit Configuration

st.set_page_config(
    page_title="PDF RAG Chatbot",
    page_icon="📂"
)


# Application Title

st.title("PDF RAG Chatbot")

st.write("Upload PDF and ask questions.")


# Create Data Folder

os.makedirs("data", exist_ok=True)


# PDF Upload

uploaded_file = st.file_uploader(
    "Upload your PDF",
    type=["pdf"]
)


# Process PDF

if uploaded_file is not None:

    if st.button("Process PDF"):

        # Save PDF

        pdf_path = os.path.join(
            "data",
            uploaded_file.name
        )

        with open(pdf_path, "wb") as f:

            f.write(uploaded_file.getbuffer())


        # Call Ingestion Function

        with st.spinner("Processing PDF..."):

            result = ingest_pdf(pdf_path)

            st.success(result)


# Ask Question

question = st.text_input("Ask your question")


# Generate Answer

if st.button("Submit Question"):

    if question:

        with st.spinner("Generating answer..."):
            collection_name = os.path.splitext(uploaded_file.name)[0].lower()

            collection_name = collection_name.replace("-", "_").replace(" ", "_")
            answer = ask_question(question, collection_name)

            st.subheader("AI Answer")

            st.write(answer)

    else:

        st.warning("Please enter a question.")