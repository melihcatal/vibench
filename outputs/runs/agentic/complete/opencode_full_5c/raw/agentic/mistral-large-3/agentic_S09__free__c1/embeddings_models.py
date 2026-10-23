from typing import List, Union, Optional
from pydantic import BaseModel


class EmbeddingObject(BaseModel):
    object: str
    embedding: List[float]
    index: int


class EmbeddingData(BaseModel):
    data: List[EmbeddingObject]
    model: str
    object: str
    usage: Optional[dict] = None


class EmbeddingRequest(BaseModel):
    input: Union[str, List[str]]
    model: str


class EmbeddingResponse(BaseModel):
    data: List[EmbeddingObject]
    model: str
    object: str
    usage: Optional[dict] = None


def normalize_embedding(embedding: List[float]) -> List[float]:
    """
    Normalizes an embedding vector to unit length.

    Args:
        embedding: Input embedding vector.

    Returns:
        Normalized embedding vector.
    """
    norm = sum(x**2 for x in embedding) ** 0.5
    return [x / norm for x in embedding] if norm != 0 else embedding
