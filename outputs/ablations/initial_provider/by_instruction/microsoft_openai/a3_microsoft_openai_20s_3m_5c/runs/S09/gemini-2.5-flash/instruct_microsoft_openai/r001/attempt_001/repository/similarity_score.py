import numpy as np
from typing import List

def cosine_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)
    similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    return float(similarity)

def similarity_score(text1_embedding: List[float], text2_embedding: List[float]) -> float:
    return cosine_similarity(text1_embedding, text2_embedding)
