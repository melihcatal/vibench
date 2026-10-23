from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Sequence


@dataclass
class EmbeddingRequest:
    model: str
    input: Any


@dataclass
class EmbeddingResponse:
    embeddings: List[Sequence[float]]
    model: str | None = None


def normalize_embedding_response(response: Any) -> List[Sequence[float]]:
    if hasattr(response, "data"):
        return [item.embedding for item in response.data]
    if isinstance(response, dict) and "data" in response:
        return [item["embedding"] for item in response["data"]]
    if isinstance(response, Iterable):
        return list(response)
    raise TypeError("Unsupported embedding response type")
