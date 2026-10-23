from typing import List, Optional, Union
from pydantic import BaseModel, Field
import numpy as np


class EmbedRequest(BaseModel):
    texts: List[str] = Field(..., min_items=1)
    model: str = "embed-multilingual-v3.0"
    input_type: str = "search_document"


class EmbedResponse(BaseModel):
    embeddings: List[List[float]]


def normalize_embedding(embedding: List[float]) -> List[float]:
    arr = np.array(embedding, dtype=np.float32)
    norm = np.linalg.norm(arr)
    if norm == 0:
        return embedding
    return (arr / norm).tolist()


def cosine_similarity(a: List[float], b: List[float]) -> float:
    a_arr = np.array(a, dtype=np.float32)
    b_arr = np.array(b, dtype=np.float32)
    dot_product = np.dot(a_arr, b_arr)
    norm_a = np.linalg.norm(a_arr)
    norm_b = np.linalg.norm(b_arr)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(dot_product / (norm_a * norm_b))
