import numpy as np
from typing import List

def normalize_embeddings(embeddings: List[List[float]]) -> np.ndarray:
    """Normalizes a list of embedding vectors to unit length."""
    np_embeddings = np.array(embeddings)
    norms = np.linalg.norm(np_embeddings, axis=1, keepdims=True)
    return np_embeddings / norms

def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Computes cosine similarity between two vectors."""
    if not isinstance(vec1, np.ndarray):
        vec1 = np.array(vec1)
    if not isinstance(vec2, np.ndarray):
        vec2 = np.array(vec2)
    
    # Ensure vectors are 1D
    vec1 = vec1.flatten()
    vec2 = vec2.flatten()

    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0
        
    return dot_product / (norm_vec1 * norm_vec2)
