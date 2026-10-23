import numpy as np
from typing import List
from .embed_text import embed_text


def cosine_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """Compute cosine similarity between two embedding vectors."""
    emb1 = np.array(embedding1)
    emb2 = np.array(embedding2)
    return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))


def similarity_score(text1: str, text2: str) -> float:
    """Compute cosine similarity between two texts using their embeddings."""
    embedding1 = embed_text(text1)
    embedding2 = embed_text(text2)
    return cosine_similarity(embedding1, embedding2)
