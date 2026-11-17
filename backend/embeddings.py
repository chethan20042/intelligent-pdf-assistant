
from sentence_transformers import SentenceTransformer


# Load the embedding model
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


def generate_embeddings(texts):

    # Convert text into numerical vectors
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    return embeddings
