from typing import List, Dict, Any
from pydantic import BaseModel

class EmbeddingRequest(BaseModel):
    input: List[str] | str
    model: str = "text-embedding-3-small"

class EmbeddingResponseItem(BaseModel):
    embedding: List[float]
    index: int
    object: str

class EmbeddingResponse(BaseModel):
    data: List[EmbeddingResponseItem]
    model: str
    object: str
    usage: Dict[str, int]

def normalize_embedding(embedding: List[float]) -> List[float]:
    import numpy as np
    arr = np.array(embedding)
    norm = np.linalg.norm(arr)
    return (arr / norm).tolist()