import numpy as np
from typing import List, Union

MODEL_ID = 'text-embedding-3-small'

def create_request(input_data: Union[str, List[str]]) -> dict:
    return {
        'model': MODEL_ID,
        'input': input_data
    }

def normalize_embedding(embedding: List[float]) -> np.ndarray:
    arr = np.array(embedding)
    norm = np.linalg.norm(arr)
    if norm == 0:
        return arr
    return arr / norm

def cosine_similarity(emb1: np.ndarray, emb2: np.ndarray) -> float:
    return np.dot(emb1, emb2)
