from dataclasses import dataclass, field
from typing import Any


@dataclass
class EmbeddingRequest:
    input: str | list[str]
    model: str = "text-embedding-3-small"
    encoding_format: str = "float"
    dimensions: int | None = None
    user: str | None = None

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "input": self.input,
            "model": self.model,
            "encoding_format": self.encoding_format,
        }
        if self.dimensions is not None:
            payload["dimensions"] = self.dimensions
        if self.user is not None:
            payload["user"] = self.user
        return payload


@dataclass
class EmbeddingData:
    index: int
    embedding: list[float]
    object_type: str = "embedding"


@dataclass
class EmbeddingUsage:
    prompt_tokens: int
    total_tokens: int


@dataclass
class EmbeddingResponse:
    object_type: str = "list"
    data: list[EmbeddingData] = field(default_factory=list)
    model: str = ""
    usage: EmbeddingUsage | None = None


def build_embedding_request(
    text: str,
    model: str = "text-embedding-3-small",
    dimensions: int | None = None,
) -> EmbeddingRequest:
    return EmbeddingRequest(input=text, model=model, dimensions=dimensions)


def build_batch_embedding_request(
    texts: list[str],
    model: str = "text-embedding-3-small",
    dimensions: int | None = None,
) -> EmbeddingRequest:
    return EmbeddingRequest(input=texts, model=model, dimensions=dimensions)


def normalize_embeddings(
    embeddings: list[list[float]],
    method: str = "l2",
) -> list[list[float]]:
    import math

    normalized = []
    for vec in embeddings:
        if method == "l2":
            norm = math.sqrt(sum(x * x for x in vec))
            if norm > 0:
                normalized.append([x / norm for x in vec])
            else:
                normalized.append(vec)
        elif method == "minmax":
            min_val = min(vec)
            max_val = max(vec)
            range_val = max_val - min_val
            if range_val > 0:
                normalized.append([(x - min_val) / range_val for x in vec])
            else:
                normalized.append(vec)
        else:
            normalized.append(vec)
    return normalized


def truncate_embedding(embedding: list[float], target_dim: int) -> list[float]:
    return embedding[:target_dim]
