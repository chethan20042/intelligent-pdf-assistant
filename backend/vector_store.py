
import chromadb
from pathlib import Path


# ----------------------------------
# CHROMADB CONFIGURATION
# ----------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_PATH = BASE_DIR / "chroma_db"

client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

collection = client.get_or_create_collection(
    name="pdf_documents"
)


# ----------------------------------
# STORE EMBEDDINGS
# ----------------------------------

def store_embeddings(chunks, embeddings, document_id):

    if not document_id:
        raise ValueError("Document ID is required.")

    if not chunks:
        raise ValueError("No chunks provided.")

    if len(chunks) != len(embeddings):
        raise ValueError(
            "Number of chunks and embeddings must match."
        )

    ids = []
    documents = []
    metadatas = []

    for chunk in chunks:

        # Create unique ID for each PDF chunk
        unique_id = f"{document_id}_{chunk['chunk_id']}"

        ids.append(unique_id)
        documents.append(chunk["text"])

        metadatas.append({
            "page": chunk["page"],
            "chunk_id": chunk["chunk_id"],
            "document_id": document_id
        })

    # Store embeddings in ChromaDB
    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

    print(f"Successfully stored {len(ids)} chunks!")

    return len(ids)


# ----------------------------------
# GET COLLECTION
# ----------------------------------

def get_collection():
    return collection
