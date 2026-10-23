import numpy as np
from typing import List

# This file can be used for custom request/response models
# or helper functions for processing embedding data.

def normalize_embeddings(embeddings: List[List[float]]) -> np.ndarray:
    """
    Normalize a list of embedding vectors.
    """
    return np.array(embeddings) / np.linalg.norm(embeddings, axis=1, keepdims=True)

def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Computes the cosine similarity between two vectors.
    Assumes vectors are 1-D numpy arrays.
    """
    # Ensure they are flat vectors
    vec1 = vec1.flatten()
    vec2 = vec2.flatten()
    
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0
        
    return dot_product / (norm_vec1 * norm_vec2)
