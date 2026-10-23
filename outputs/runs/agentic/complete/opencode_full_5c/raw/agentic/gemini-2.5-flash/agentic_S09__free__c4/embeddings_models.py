import numpy as np
from typing import List, Dict, Union


def normalize_embedding(embedding: List[float]) -> List[float]:
    """Normalizes an embedding vector."""
    norm = np.linalg.norm(embedding)
    if norm == 0:
        return embedding
    return (np.array(embedding) / norm).tolist()


def calculate_cosine_similarity(
    embedding1: List[float], embedding2: List[float]
) -> float:
    """Calculates cosine similarity between two embedding vectors."""
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0
    return dot_product / (norm_vec1 * norm_vec2)


class TextEmbeddingRequest:
    def __init__(self, text: str):
        self.text = text


class TextEmbeddingResponse:
    def __init__(self, embedding: List[float]):
        self.embedding = embedding


class BatchTextEmbeddingRequest:
    def __init__(self, texts: List[str]):
        self.texts = texts


class BatchTextEmbeddingResponse:
    def __init__(self, embeddings: List[List[float]]):
        self.embeddings = embeddings
