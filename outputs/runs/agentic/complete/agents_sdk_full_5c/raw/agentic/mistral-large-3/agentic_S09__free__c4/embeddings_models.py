from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class EmbeddingRequest(BaseModel):
    input: List[str] = Field(..., min_items=1)
    model: str = "text-embedding-3-small"

class EmbeddingResponseItem(BaseModel):
    embedding: List[float]
    index: int

class EmbeddingResponse(BaseModel):
    data: List[EmbeddingResponseItem]
    model: str
    usage: Dict[str, int]

def normalize_embedding(embedding: List[float]) -> List[float]:
    import numpy as np
    arr = np.array(embedding)
    norm = np.linalg.norm(arr)
    return (arr / norm).tolist() if norm > 0 else arr.tolist()