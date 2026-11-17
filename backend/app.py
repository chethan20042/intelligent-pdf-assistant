
import streamlit as st
import tempfile
import os
import hashlib

from pdf_processor import extract_text_from_pdf
from chunking import create_chunks
from embeddings import generate_embeddings
from vector_store import store_embeddings
from rag_pipeline import ask_pdf_question


# ----------------------------------
# PAGE CONFIGURATION
# ----------------------------------

st.set_page_config(
    page_title="Intelligent PDF Assistant",
    page_icon="📄",
    layout="wide"
)


# ----------------------------------
# APPLICATION HEADER
# ----------------------------------

st.title("📄 Intelligent PDF Assistant")

st.write(
    "Upload your PDF and ask questions. "
    "Get AI-powered answers based on your document."
)

st.divider()


# ----------------------------------
# INITIALIZE SESSION STATE
# ----------------------------------

if "processed" not in st.session_state:
    st.session_state["processed"] = False

if "document_id" not in st.session_state:
    st.session_state["document_id"] = None

if "filename" not in st.session_state:
    st.session_state["filename"] = None

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


# ----------------------------------
# PDF UPLOAD
# ----------------------------------

uploaded_file = st.file_uploader(
    "Upload your PDF document",
    type=["pdf"]
)


if uploaded_file is not None:

    st.success(f"Uploaded: {uploaded_file.name}")

    pdf_bytes = uploaded_file.getvalue()

    document_id = hashlib.sha256(pdf_bytes).hexdigest()

    # Clear old processing state when a different PDF is selected
    if (
        st.session_state["document_id"] is not None
        and st.session_state["document_id"] != document_id
    ):
        st.session_state["processed"] = False
        st.session_state["document_id"] = None
        st.session_state["filename"] = None
        st.session_state["chat_history"] = []

    # ----------------------------------
    # PROCESS PDF
    # ----------------------------------

    if st.button("Process PDF", type="primary"):

        temp_path = None

        try:

            with st.spinner("Processing your PDF..."):

                # Save PDF temporarily
                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                ) as temp_file:

                    temp_file.write(pdf_bytes)
                    temp_path = temp_file.name

                # Step 1: Extract text
                pages = extract_text_from_pdf(temp_path)

                if not pages:
                    raise ValueError(
                        "No readable text found in this PDF."
                    )

                # Step 2: Create chunks
                chunks = create_chunks(pages)

                if not chunks:
                    raise ValueError(
                        "No text chunks could be created."
                    )

                # Step 3: Generate embeddings
                texts = [
                    chunk["text"] for chunk in chunks
                ]

                embeddings = generate_embeddings(texts)

                # Step 4: Store embeddings
                total_chunks = store_embeddings(
                    chunks,
                    embeddings,
                    document_id
                )

                # Save processing information
                st.session_state["document_id"] = document_id
                st.session_state["filename"] = uploaded_file.name
                st.session_state["processed"] = True

                # Reset chat for newly processed document
                st.session_state["chat_history"] = []

            st.success("PDF processed successfully!")

            st.write(f"Pages extracted: {len(pages)}")
            st.write(f"Chunks created: {len(chunks)}")
            st.write(f"Embeddings stored: {total_chunks}")

        except Exception as e:

            st.session_state["processed"] = False
            st.session_state["document_id"] = None
            st.session_state["chat_history"] = []

            st.error(f"PDF processing failed: {e}")

        finally:

            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)


# ----------------------------------
# CHAT INTERFACE
# ----------------------------------

if uploaded_file is not None:

    current_document_id = hashlib.sha256(
        uploaded_file.getvalue()
    ).hexdigest()

    if (
        st.session_state["processed"]
        and st.session_state["document_id"] == current_document_id
    ):

        st.divider()

        st.subheader("💬 Chat with Your PDF")

        # Clear conversation button
        if st.button("🗑️ Clear Chat"):

            st.session_state["chat_history"] = []
            st.rerun()

        # Display previous conversation
        for message in st.session_state["chat_history"]:

            with st.chat_message(message["role"]):

                st.markdown(message["content"])

                # Display source pages for assistant messages
                if (
                    message["role"] == "assistant"
                    and message.get("sources")
                ):

                    st.caption("📚 Source Pages")

                    for page in message["sources"]:
                        st.write(f"📄 Page {page}")

        # User question input
        question = st.chat_input(
            "Ask a question about your PDF..."
        )

        if question:

            # Display user question
            with st.chat_message("user"):
                st.markdown(question)

            # Save user message
            st.session_state["chat_history"].append({
                "role": "user",
                "content": question
            })

            try:

                with st.chat_message("assistant"):

                    with st.spinner("Thinking..."):

                        result = ask_pdf_question(
                            question=question,
                            document_id=st.session_state["document_id"],
                            chat_history=st.session_state["chat_history"][:-1]
                        )

                    st.markdown(result["answer"])

                    if result["sources"]:

                        st.caption("📚 Source Pages")

                        for page in result["sources"]:
                            st.write(f"📄 Page {page}")

                    # Save assistant response
                    st.session_state["chat_history"].append({
                        "role": "assistant",
                        "content": result["answer"],
                        "sources": result["sources"]
                    })

            except Exception as e:

                st.error(f"Error generating answer: {e}")

