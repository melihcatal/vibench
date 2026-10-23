import dataclasses
from typing import List


@dataclasses.dataclass
class EmbeddingRequest:
    input: List[str]
    model: str = "text-embedding-ada-002"


@dataclasses.dataclass
class EmbeddingResponseData:
    embedding: List[float]
    index: int
    object: str


@dataclasses.dataclass
class EmbeddingResponse:
    data: List[EmbeddingResponseData]
    model: str
    object: str
    usage: dict


def normalize_embedding(embedding: List[float]) -> List[float]:
    """Normalizes an embedding vector to unit length."""
    import numpy as np

    return (embedding / np.linalg.norm(embedding)).tolist()
