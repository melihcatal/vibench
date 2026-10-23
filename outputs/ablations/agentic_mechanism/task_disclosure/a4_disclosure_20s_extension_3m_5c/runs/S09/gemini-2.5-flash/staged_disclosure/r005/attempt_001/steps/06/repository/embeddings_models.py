import dataclasses
from typing import List
import numpy as np

@dataclasses.dataclass
class EmbeddingRequest:
    text: str

@dataclasses.dataclass
class EmbeddingResponse:
    embedding: List[float]

def normalize_embedding(embedding: List[float]) -> List[float]:
    """
    Normalizes an embedding vector using L2 normalization.
    """
    np_embedding = np.array(embedding)
    norm = np.linalg.norm(np_embedding)
    if norm == 0:
        return embedding
    normalized_embedding = (np_embedding / norm).tolist()
    return normalized_embedding
