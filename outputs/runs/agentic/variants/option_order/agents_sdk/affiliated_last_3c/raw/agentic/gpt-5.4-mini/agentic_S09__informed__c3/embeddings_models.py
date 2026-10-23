from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Sequence


@dataclass
class EmbeddingRequest:
    text: str
    model: str = "text-embedding-3-small"


@dataclass
class EmbeddingBatchRequest:
    texts: List[str]
    model: str = "text-embedding-3-small"


@dataclass
class EmbeddingResponse:
    vector: List[float]
    model: str
    provider: str = "openai"


@dataclass
class EmbeddingBatchResponse:
    vectors: List[List[float]]
    model: str
    provider: str = "openai"


@dataclass
class SearchDocument:
    id: str
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SearchQueryBundle:
    query: str
    query_vector: List[float]
    documents: List[SearchDocument]
    document_vectors: List[List[float]]


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).split())


def normalize_texts(values: Sequence[Any]) -> List[str]:
    return [normalize_text(value) for value in values]


def ensure_float_vector(values: Sequence[Any]) -> List[float]:
    return [float(v) for v in values]
