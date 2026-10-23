from dataclasses import dataclass
from typing import Any, Iterable


@dataclass(frozen=True)
class EmbeddingRequest:
    texts: list[str]
    model: str


@dataclass(frozen=True)
class EmbeddingResponse:
    embeddings: list[list[float]]
    model: str | None = None


@dataclass(frozen=True)
class NormalizedEmbedding:
    values: list[float]


def normalize_embedding_response(response: Any) -> list[list[float]]:
    data = getattr(response, "data", response)
    embeddings: list[list[float]] = []
    for item in data:
        vector = getattr(item, "embedding", item)
        embeddings.append([float(x) for x in vector])
    return embeddings


def normalize_texts(texts: Iterable[str]) -> list[str]:
    return [str(text).strip() for text in texts if str(text).strip()]
