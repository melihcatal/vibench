import os
from typing import List
import cohere


def embed_translated_segments(
    segments: List[str], model: str = "embed-english-v3.0"
) -> List[List[float]]:
    """
    Embed translated segments for translation-memory search using Cohere Embeddings.

    Args:
        segments: List of translated text segments to embed
        model: Cohere embedding model to use

    Returns:
        List of embedding vectors
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable is required")

    client = cohere.Client(api_key)

    response = client.embed(texts=segments, model=model, input_type="search_document")

    return response.embeddings


def find_similar_translations(
    query: str, embeddings: List[List[float]], segments: List[str], top_k: int = 5
) -> List[dict]:
    """
    Find similar translations using embedded segments.

    Args:
        query: Query text to find similar translations for
        embeddings: List of embedding vectors for existing segments
        segments: Original text segments corresponding to embeddings
        top_k: Number of similar results to return

    Returns:
        List of similar translations with similarity scores
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable is required")

    client = cohere.Client(api_key)

    query_response = client.embed(
        texts=[query], model="embed-english-v3.0", input_type="search_query"
    )

    query_embedding = query_response.embeddings[0]

    import numpy as np

    similarities = []
    for i, emb in enumerate(embeddings):
        similarity = np.dot(query_embedding, emb) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(emb)
        )
        similarities.append(
            {"segment": segments[i], "similarity": float(similarity), "index": i}
        )

    similarities.sort(key=lambda x: x["similarity"], reverse=True)

    return similarities[:top_k]
