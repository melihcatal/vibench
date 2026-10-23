import numpy as np
from embeddings_client import get_embeddings_client
from typing import List


def get_embedding(text: str, client) -> List[float]:
    """Helper to get embedding for a single text."""
    result = client.embed_content(
        model="models/embedding-001", content=text, task_type="semantic_similarity"
    )
    return result["embedding"]


def calculate_similarity_score(text1: str, text2: str) -> float:
    """
    Computes cosine similarity between two embedded texts using Gemini API.
    """
    client = get_embeddings_client()

    embedding1 = get_embedding(text1, client)
    embedding2 = get_embedding(text2, client)

    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)

    similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    return float(similarity)
