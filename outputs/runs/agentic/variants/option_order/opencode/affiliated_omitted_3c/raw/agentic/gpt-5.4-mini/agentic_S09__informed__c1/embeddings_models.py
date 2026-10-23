from dataclasses import dataclass
from typing import Any, Dict, List, Sequence


@dataclass
class EmbeddingRequest:
    inputs: Sequence[str]
    model: str = "text-embedding-3-small"


@dataclass
class EmbeddingResponse:
    embeddings: List[List[float]]
    model: str


def normalize_vector(values: Sequence[Any]) -> List[float]:
    return [float(v) for v in values]


def normalize_embeddings(payload: Dict[str, Any]) -> EmbeddingResponse:
    data = payload.get("data", payload.get("embeddings", []))
    embeddings: List[List[float]] = []
    for item in data:
        vector = item.get("embedding", item if isinstance(item, list) else [])
        embeddings.append(normalize_vector(vector))
    return EmbeddingResponse(
        embeddings=embeddings, model=str(payload.get("model", "text-embedding-3-small"))
    )
