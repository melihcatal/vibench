import os
import numpy as np
from typing import List
from openai import OpenAI
from model_client import get_client


def embed_text(text: str) -> List[float]:
    """
    Embed model outputs for clustering or retrieval using OpenAI embeddings.
    """
    client = get_client()

    try:
        response = client.embeddings.create(model="text-embedding-3-small", input=text)

        embedding = response.data[0].embedding
        return embedding
    except Exception as e:
        raise Exception(f"Failed to create embedding: {str(e)}")


def embed_batch(texts: List[str]) -> List[List[float]]:
    """
    Embed multiple texts in batch.
    """
    client = get_client()

    try:
        response = client.embeddings.create(model="text-embedding-3-small", input=texts)

        embeddings = [item.embedding for item in response.data]
        return embeddings
    except Exception as e:
        raise Exception(f"Failed to create batch embeddings: {str(e)}")


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two embeddings.
    """
    vec1_np = np.array(vec1)
    vec2_np = np.array(vec2)

    dot_product = np.dot(vec1_np, vec2_np)
    norm1 = np.linalg.norm(vec1_np)
    norm2 = np.linalg.norm(vec2_np)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return float(dot_product / (norm1 * norm2))
