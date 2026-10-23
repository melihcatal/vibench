from dataclasses import dataclass
from typing import List


@dataclass
class EmbeddingRequest:
    text: str


@dataclass
class EmbeddingBatchRequest:
    texts: List[str]


@dataclass
class EmbeddingResponse:
    embedding: List[float]
