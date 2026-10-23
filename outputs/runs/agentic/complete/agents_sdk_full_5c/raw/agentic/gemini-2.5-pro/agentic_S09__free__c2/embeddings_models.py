from typing import List, NamedTuple
import numpy as np

# Google's text-embedding-004 is a recommended model.
GOOGLE_EMBEDDING_MODEL = "text-embedding-004"

class EmbeddingResponse(NamedTuple):
    text: str
    vector: List[float]

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Computes the cosine similarity between two vectors."""
    vec1 = np.array(v1)
    vec2 = np.array(v2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
