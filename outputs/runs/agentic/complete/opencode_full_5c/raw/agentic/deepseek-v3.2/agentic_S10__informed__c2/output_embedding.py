import os
import numpy as np
from typing import List
from openai import OpenAI


def embed_text(text: str, model: str = "text-embedding-3-small") -> List[float]:
    """
    Embed model outputs for clustering or retrieval using OpenAI embeddings.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.embeddings.create(
        model=model, input=text, encoding_format="float"
    )

    return response.data[0].embedding


def embed_batch(
    texts: List[str], model: str = "text-embedding-3-small"
) -> List[List[float]]:
    """
    Embed multiple texts in batch.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.embeddings.create(
        model=model, input=texts, encoding_format="float"
    )

    return [item.embedding for item in response.data]


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two embedding vectors.
    """
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return float(dot_product / (norm1 * norm2))


def find_similar_embeddings(
    query_embedding: List[float], embeddings: List[List[float]], top_k: int = 5
) -> List[int]:
    """
    Find most similar embeddings to query embedding.
    """
    similarities = []

    for i, emb in enumerate(embeddings):
        sim = cosine_similarity(query_embedding, emb)
        similarities.append((i, sim))

    # Sort by similarity (descending)
    similarities.sort(key=lambda x: x[1], reverse=True)

    # Return indices of top_k most similar
    return [idx for idx, _ in similarities[:top_k]]
