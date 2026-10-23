from dataclasses import dataclass
from typing import Any, Iterable, List, Sequence


@dataclass
class EmbeddingRequest:
    input: Any
    model: str = "text-embedding-3-small"


@dataclass
class EmbeddingResponse:
    vectors: List[List[float]]
    model: str


def normalize_embedding(value: Sequence[Any]) -> List[float]:
    return [float(x) for x in value]


def normalize_embeddings(values: Iterable[Sequence[Any]]) -> List[List[float]]:
    return [normalize_embedding(v) for v in values]
