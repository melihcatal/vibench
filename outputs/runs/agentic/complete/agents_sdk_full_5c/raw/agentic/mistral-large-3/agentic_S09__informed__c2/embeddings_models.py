from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class EmbeddingRequest(BaseModel):
    input: List[str] = Field(..., min_items=1)
    model: str = "text-embedding-v2"  # DashScope's text-embedding-v2


class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]] = Field(..., description="List of embedding vectors")
    usage: Dict[str, int] = Field(..., description="Token usage statistics")
    request_id: Optional[str] = Field(None, description="Request identifier")


def normalize_embedding(embedding: List[float]) -> List[float]:
    """Normalize embedding vector to unit length."""
    import numpy as np
    norm = np.linalg.norm(embedding)
    return (np.array(embedding) / norm).tolist()