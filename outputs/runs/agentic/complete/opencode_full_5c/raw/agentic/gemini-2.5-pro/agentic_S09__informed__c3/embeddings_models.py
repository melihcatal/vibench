from typing import List, Union
from pydantic import BaseModel


class EmbeddingRequest(BaseModel):
    input: Union[str, List[str]]
    model: str = "text-embedding-3-small"


class EmbeddingData(BaseModel):
    embedding: List[float]
    index: int
    object: str


class EmbeddingUsage(BaseModel):
    prompt_tokens: int
    total_tokens: int


class EmbeddingResponse(BaseModel):
    data: List[EmbeddingData]
    model: str
    object: str
    usage: EmbeddingUsage


def normalize_vector(vector: List[float]) -> List[float]:
    norm = sum(v**2 for v in vector) ** 0.5
    if norm == 0:
        return vector
    return [v / norm for v in vector]
