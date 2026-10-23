from typing import List
import numpy as np


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Compute cosine similarity between two embedding vectors."""
    vec1_arr = np.array(vec1)
    vec2_arr = np.array(vec2)
    dot_product = np.dot(vec1_arr, vec2_arr)
    norm_product = np.linalg.norm(vec1_arr) * np.linalg.norm(vec2_arr)
    return float(dot_product / norm_product)