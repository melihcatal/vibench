import numpy as np
from typing import List
from embed_text import embed_text

def cosine_similarity(a: List[float], b: List[float]) -> float:
    a_array = np.array(a)
    b_array = np.array(b)
    dot_product = np.dot(a_array, b_array)
    norm_a = np.linalg.norm(a_array)
    norm_b = np.linalg.norm(b_array)
    return dot_product / (norm_a * norm_b)

def similarity_score(text1: str, text2: str) -> float:
    embedding1 = embed_text(text1)
    embedding2 = embed_text(text2)
    return cosine_similarity(embedding1, embedding2)