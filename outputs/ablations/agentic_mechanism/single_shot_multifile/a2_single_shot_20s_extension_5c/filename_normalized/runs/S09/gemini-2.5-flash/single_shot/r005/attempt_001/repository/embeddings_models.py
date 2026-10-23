from typing import List, Dict
import math

class EmbeddingRequest:
    def __init__(self, texts: List[str], model: str = None):
        self.texts = texts
        self.model = model

class EmbeddingResponse:
    def __init__(self, embeddings: List[List[float]], model: str = None):
        self.embeddings = embeddings
        self.model = model

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    dot_product = sum(v1 * v2 for v1, v2 in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(v1 * v1 for v1 in vec1))
    magnitude2 = math.sqrt(sum(v2 * v2 for v2 in vec2))
    if not magnitude1 or not magnitude2:
        return 0.0
    return dot_product / (magnitude1 * magnitude2)
