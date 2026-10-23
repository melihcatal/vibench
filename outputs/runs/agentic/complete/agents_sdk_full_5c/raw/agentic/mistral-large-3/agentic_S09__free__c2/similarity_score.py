from typing import List
import numpy as np


def cosine_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """Compute cosine similarity between two embeddings."""
    arr1 = np.array(embedding1, dtype=np.float32)
    arr2 = np.array(embedding2, dtype=np.float32)
    dot_product = np.dot(arr1, arr2)
    norm1 = np.linalg.norm(arr1)
    norm2 = np.linalg.norm(arr2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return float(dot_product / (norm1 * norm2))


def similarity_score(text_embedding1: List[float], text_embedding2: List[float]) -> float:
    """Compute cosine similarity between two embedded texts."""
    return cosine_similarity(text_embedding1, text_embedding2)