from dataclasses import dataclass
from typing import Any, Iterable, List, Sequence


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def normalize_texts(values: Iterable[Any]) -> List[str]:
    return [normalize_text(v) for v in values]


def cosine_similarity(vector_a: Sequence[float], vector_b: Sequence[float]) -> float:
    if len(vector_a) != len(vector_b) or not vector_a:
        return 0.0
    dot = sum(a * b for a, b in zip(vector_a, vector_b))
    norm_a = sum(a * a for a in vector_a) ** 0.5
    norm_b = sum(b * b for b in vector_b) ** 0.5
    if not norm_a or not norm_b:
        return 0.0
    return dot / (norm_a * norm_b)


@dataclass
class EmbeddingRequest:
    text: str


@dataclass
class EmbeddingBatchRequest:
    texts: List[str]


@dataclass
class EmbeddingResponse:
    embedding: List[float]


@dataclass
class EmbeddingBatchResponse:
    embeddings: List[List[float]]
