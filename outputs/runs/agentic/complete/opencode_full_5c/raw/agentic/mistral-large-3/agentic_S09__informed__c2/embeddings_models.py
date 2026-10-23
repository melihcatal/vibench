from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class EmbeddingRequest(BaseModel):
    text: str = Field(..., description="Input text to embed")
    model: str = Field(
        "text-embedding-v2", description="Model identifier for DashScope"
    )


class BatchEmbeddingRequest(BaseModel):
    texts: List[str] = Field(..., description="List of input texts to embed")
    model: str = Field(
        "text-embedding-v2", description="Model identifier for DashScope"
    )


class EmbeddingResponse(BaseModel):
    embedding: List[float] = Field(..., description="Generated embedding vector")
    model: str = Field(..., description="Model identifier used for generation")


class BatchEmbeddingResponse(BaseModel):
    embeddings: List[List[float]] = Field(
        ..., description="List of generated embedding vectors"
    )
    model: str = Field(..., description="Model identifier used for generation")


def normalize_embedding(embedding: List[float]) -> List[float]:
    """Normalize embedding vector to unit length."""
    import numpy as np

    norm = np.linalg.norm(embedding)
    return (np.array(embedding) / norm).tolist() if norm > 0 else embedding
