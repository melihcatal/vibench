import numpy as np
from typing import List


def cosine_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """
    Compute cosine similarity between two embedding vectors.
    
    Args:
        embedding1: First embedding vector.
        embedding2: Second embedding vector.
    
    Returns:
        Cosine similarity score as a float.
    """
    arr1 = np.array(embedding1, dtype=np.float32)
    arr2 = np.array(embedding2, dtype=np.float32)
    return float(np.dot(arr1, arr2) / (np.linalg.norm(arr1) * np.linalg.norm(arr2)))


def similarity_score(text_embedding1: List[float], text_embedding2: List[float]) -> float:
    """
    Compute similarity score between two embedded texts using cosine similarity.
    
    Args:
        text_embedding1: Embedding vector of the first text.
        text_embedding2: Embedding vector of the second text.
    
    Returns:
        Similarity score as a float.
    """
    return cosine_similarity(text_embedding1, text_embedding2)