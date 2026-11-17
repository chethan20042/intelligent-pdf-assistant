
from embeddings import generate_embeddings
from vector_store import get_collection


def search_documents(question, document_id, top_k=3, threshold=0.75):

    if not question or not question.strip():
        raise ValueError("Question cannot be empty")

    if not document_id:
        raise ValueError("Document ID is required")

    question_embedding = generate_embeddings([question])
    collection = get_collection()

    results = collection.query(
        query_embeddings=question_embedding.tolist(),
        n_results=top_k,
        where={"document_id": document_id}
    )

    # DEBUG: Inspect raw retrieval results
    print("\n========== RETRIEVAL DEBUG ==========")
    print("Document ID:", document_id)
    print("Matching chunks:", len(results["documents"][0]))
    print("Raw distances:", results["distances"][0])

    for i, distance in enumerate(results["distances"][0]):
        print(f"\nResult {i + 1}")
        print("Distance:", distance)
        print("Page:", results["metadatas"][0][i]["page"])
        print("Text:", results["documents"][0][i][:200])

    print("Threshold:", threshold)
    print("=====================================\n")

    # Filter results by distance
    filtered_results = {
        "ids": [[]],
        "documents": [[]],
        "metadatas": [[]],
        "distances": [[]]
    }

    for i, distance in enumerate(results["distances"][0]):

        if distance <= threshold:
            filtered_results["ids"][0].append(
                results["ids"][0][i]
            )
            filtered_results["documents"][0].append(
                results["documents"][0][i]
            )
            filtered_results["metadatas"][0].append(
                results["metadatas"][0][i]
            )
            filtered_results["distances"][0].append(distance)

    print(
        "Relevant chunks after filtering:",
        len(filtered_results["documents"][0])
    )

    return filtered_results
