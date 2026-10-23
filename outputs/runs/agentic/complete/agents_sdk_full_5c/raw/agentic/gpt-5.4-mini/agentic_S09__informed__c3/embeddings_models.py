from dataclasses import dataclass, field
from typing import Any, Iterable, Sequence


@dataclass(frozen=True)
class EmbeddingRequest:
    texts: Sequence[str]
    model: str
    input_type: str = "search_document"


@dataclass(frozen=True)
class EmbeddingResponse:
    embeddings: list[list[float]]
    model: str


@dataclass(frozen=True)
class SearchEmbeddingBundle:
    query: list[float]
    documents: list[list[float]]
    query_text: str = ""
    document_texts: tuple[str, ...] = field(default_factory=tuple)


def normalize_embedding(values: Iterable[Any]) -> list[float]:
    return [float(value) for value in values]


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    if len(a) != len(b):
        raise ValueError("Embedding vectors must have the same length")
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)
