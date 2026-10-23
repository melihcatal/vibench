from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class EmbeddingRequest(BaseModel):
    text: str
    task_type: Optional[str] = "retrieval_document"


class BatchEmbeddingRequest(BaseModel):
    texts: List[str]
    task_type: Optional[str] = "retrieval_document"


class EmbeddingResponse(BaseModel):
    embedding: List[float]
    model: Optional[str] = None


class BatchEmbeddingResponse(BaseModel):
    embeddings: List[List[float]]
    model: Optional[str] = None


def normalize_embedding(embedding: List[float]) -> List[float]:
    """
    Normalizes an embedding vector to unit length.
    """
    import numpy as np

    vec = np.array(embedding)
    norm = np.linalg.norm(vec)
    if norm == 0:
        return embedding
    return (vec / norm).tolist()
