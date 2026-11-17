
from retriever import search_documents
from llm import generate_answer


def ask_pdf_question(question, document_id, chat_history=None):

    # Step 1: Validate inputs
    if not question or not question.strip():
        raise ValueError("Question cannot be empty")

    if not document_id:
        raise ValueError("Document ID is required")

    # Step 2: Prepare conversation history
    if chat_history is None:
        chat_history = []

    # Keep only the most recent 4 messages
    recent_history = chat_history[-4:]

    history_context = ""

    for message in recent_history:
        role = message.get("role", "user")
        content = message.get("content", "")

        history_context += f"{role}: {content}\n"

    # Step 3: Build a contextual search query
    search_query = question

    if history_context:
        search_query = (
            f"Previous conversation:\n{history_context}\n"
            f"Current question: {question}"
        )

    # Step 4: Retrieve relevant chunks
    results = search_documents(
        question=search_query,
        document_id=document_id,
        top_k=3,
        threshold=0.75
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    # Step 5: Handle missing information
    if not documents:
        return {
            "question": question,
            "answer": "I could not find relevant information in the uploaded PDF.",
            "sources": []
        }

    # Step 6: Prepare PDF context
    context_parts = []

    for i, document in enumerate(documents):
        page = metadatas[i]["page"]

        context_parts.append(
            f"Page {page}:\n{document}"
        )

    pdf_context = "\n\n".join(context_parts)

    # Step 7: Combine conversation and PDF context
    full_context = f"""
Previous conversation:
{history_context if history_context else "No previous conversation."}

Relevant information from the uploaded PDF:
{pdf_context}
"""

    # Step 8: Generate answer
    answer = generate_answer(
        question=question,
        context=full_context
    )

    # Step 9: Collect unique source pages
    source_pages = sorted({
        metadata["page"]
        for metadata in metadatas
    })

    # Step 10: Return result
    return {
        "question": question,
        "answer": answer,
        "sources": source_pages
    }
