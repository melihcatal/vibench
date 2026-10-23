import numpy as np
from typing import List

# A simple wrapper for embedding responses
class EmbeddingResponse:
    def __init__(self, embeddings: List[List[float]], model: str):
        self.embeddings = embeddings
        self.model = model

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Computes the cosine similarity between two vectors."""
    vec1 = np.array(v1)
    vec2 = np.array(v2)
    
    # Check for zero vectors
    if np.all(vec1==0) or np.all(vec2==0):
        return 0.0

    similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    return float(similarity)
