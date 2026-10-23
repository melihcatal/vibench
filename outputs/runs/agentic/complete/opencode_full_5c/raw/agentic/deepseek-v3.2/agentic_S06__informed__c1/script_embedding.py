import os
import cohere


def embed_text(text, model="embed-english-v3.0"):
    """Embed narration scripts for voice-asset search using Cohere Embeddings."""
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable is required")

    co = cohere.Client(api_key)

    response = co.embed(texts=[text], model=model, input_type="search_document")

    return response.embeddings[0]


def embed_batch(texts, model="embed-english-v3.0"):
    """Embed multiple texts in batch."""
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable is required")

    co = cohere.Client(api_key)

    response = co.embed(texts=texts, model=model, input_type="search_document")

    return response.embeddings


def search_similar_embeddings(query_embedding, embeddings_list, top_k=5):
    """Search for similar embeddings using cosine similarity."""
    import numpy as np

    if not embeddings_list:
        return []

    query_vec = np.array(query_embedding)
    embeddings_array = np.array(embeddings_list)

    similarities = np.dot(embeddings_array, query_vec) / (
        np.linalg.norm(embeddings_array, axis=1) * np.linalg.norm(query_vec)
    )

    top_indices = np.argsort(similarities)[-top_k:][::-1]

    return [
        {"index": int(idx), "similarity": float(similarities[idx])}
        for idx in top_indices
    ]
