import numpy as np
from typing import List, Dict, Union
from dataclasses import dataclass

@dataclass
class EmbeddingsRequest:
    texts: List[str]
    model_id: str
    
@dataclass
class EmbeddingsResponse:
    embeddings: List[List[float]]
    model_id: str

def normalize_embedding(embedding: List[float]) -> List[float]:
    """
    Normalizes an embedding vector using L2 normalization.
    """
    if not embedding:
        return []
    np_embedding = np.array(embedding)
    norm = np.linalg.norm(np_embedding)
    if norm == 0:
        return np_embedding.tolist()
    return (np_embedding / norm).tolist()

