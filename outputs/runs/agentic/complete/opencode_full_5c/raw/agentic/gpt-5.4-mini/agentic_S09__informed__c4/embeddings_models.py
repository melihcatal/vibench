from dataclasses import dataclass
from typing import Any, Iterable, List, Sequence


@dataclass
class EmbeddingRequest:
    input: Sequence[str]
    model: str


@dataclass
class EmbeddingResponse:
    embeddings: List[List[float]]
    model: str


def normalize_texts(texts: Any) -> List[str]:
    if isinstance(texts, str):
        return [texts]
    return [str(text) for text in texts]


def normalize_embedding(vector: Iterable[Any]) -> List[float]:
    return [float(value) for value in vector]
