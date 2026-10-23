from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class EmbeddingRequest(BaseModel):
    texts: List[str]
    model: str = "text-embedding-3-small"
    dimensions: Optional[int] = None


class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]
    model: str
    usage: Dict[str, int]


def normalize_embedding(embedding: List[float]) -> List[float]:
    """Normalize an embedding vector to unit length."""
    norm = np.linalg.norm(embedding)
    if norm == 0:
        return embedding
    return [x / norm for x in embedding]
