
def create_chunks(pages, chunk_size=500, overlap=100):

    chunks = []

    # Validate chunking settings
    if chunk_size <= 0:
        raise ValueError("Chunk size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("Overlap must be non-negative and smaller than chunk size")

    chunk_id = 1

    # Process every PDF page
    for page_data in pages:

        text = page_data["text"]
        page_number = page_data["page"]

        # Split text into smaller chunks
        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end].strip()

            if chunk_text:

                chunks.append({
                    "chunk_id": chunk_id,
                    "page": page_number,
                    "text": chunk_text
                })

                chunk_id += 1

            # Move forward with overlap
            start += chunk_size - overlap

    return chunks
