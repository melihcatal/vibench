from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence


@dataclass
class EmbeddingRequest:
    inputs: Sequence[str]
    model: str = "text-embedding-3-small"


@dataclass
class EmbeddingResponse:
    embeddings: List[List[float]]
    model: str
    raw: Optional[Dict[str, Any]] = None


def normalize_embedding(value: Any) -> List[float]:
    if isinstance(value, dict):
        for key in ("embedding", "vector", "values", "data"):
            if key in value:
                return normalize_embedding(value[key])
    if isinstance(value, list):
        if value and isinstance(value[0], dict):
            if "embedding" in value[0]:
                return [float(x) for x in value[0]["embedding"]]
            if "vector" in value[0]:
                return [float(x) for x in value[0]["vector"]]
        return [float(x) for x in value]
    raise TypeError("Unsupported embedding format")


def normalize_embeddings(payload: Any) -> List[List[float]]:
    if isinstance(payload, dict) and "data" in payload:
        return [normalize_embedding(item) for item in payload["data"]]
    if isinstance(payload, list):
        return [normalize_embedding(item) for item in payload]
    return [normalize_embedding(payload)]
