import numpy as np
from typing import List, Union
import os
from openai import OpenAI


def embed_text_with_openai(
    text: str, model: str = "text-embedding-3-small"
) -> List[float]:
    """Helper to embed text using OpenAI API."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(
        model=model, input=text, encoding_format="float"
    )
    return response.data[0].embedding


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Compute cosine similarity between two vectors.

    Args:
        vec1: First vector
        vec2: Second vector

    Returns:
        float: Cosine similarity score between -1 and 1
    """
    v1 = np.array(vec1)
    v2 = np.array(vec2)

    dot_product = np.dot(v1, v2)
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return float(dot_product / (norm1 * norm2))


def similarity_score(
    text1: str, text2: str, model: str = "text-embedding-3-small"
) -> float:
    """
    Compute cosine similarity between two embedded texts using OpenAI embeddings.

    Args:
        text1: First text string
        text2: Second text string
        model: The OpenAI embedding model to use (default: text-embedding-3-small)

    Returns:
        float: Cosine similarity score between -1 and 1
    """
    embedding1 = embed_text_with_openai(text1, model)
    embedding2 = embed_text_with_openai(text2, model)

    return cosine_similarity(embedding1, embedding2)
