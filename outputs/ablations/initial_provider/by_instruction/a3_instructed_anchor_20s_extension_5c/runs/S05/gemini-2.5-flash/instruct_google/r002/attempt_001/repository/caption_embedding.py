from sentence_transformers import SentenceTransformer


def embed_caption_chunk(text: str):
    # Using a local sentence transformer model for embedding.
    # For a production system, consider a hosted embedding service or a more scalable solution.
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embedding = model.encode(text)
    return embedding.tolist() # Convert numpy array to list for easier serialization
