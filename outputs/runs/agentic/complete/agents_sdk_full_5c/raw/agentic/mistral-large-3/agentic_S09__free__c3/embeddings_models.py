from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class EmbeddingRequest(BaseModel):
    texts: List[str] = Field(..., min_items=1)
    model: str = "embed-english-v3.0"
    input_type: Optional[str] = None
    truncate: Optional[str] = "END"


class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]
    meta: Dict[str, Any]


def normalize_embedding(embedding: List[float]) -> List[float]:
    import numpy as np
    norm = np.linalg.norm(embedding)
    return (np.array(embedding) / norm).tolist()