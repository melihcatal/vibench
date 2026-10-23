import numpy as np
from typing import List
from embed_text import embed_text

def cosine_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    dot_product = np.dot(embedding1, embedding2)
    norm_a = np.linalg.norm(embedding1)
    norm_b = np.linalg.norm(embedding2)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)

def similarity_score(text1: str, text2: str) -> float:
    embedding_result1 = embed_text(text1)
    embedding_result2 = embed_text(text2)
    return cosine_similarity(embedding_result1.embedding, embedding_result2.embedding)
