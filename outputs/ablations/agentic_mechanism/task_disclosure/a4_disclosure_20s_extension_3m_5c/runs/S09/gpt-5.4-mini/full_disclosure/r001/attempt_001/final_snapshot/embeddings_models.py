from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence


DEFAULT_MODEL = "text-embedding-3-small"


def _coerce_text_input(texts: Any) -> Any:
    if isinstance(texts, str):
        return texts
    if isinstance(texts, Sequence):
        return [str(text) for text in texts]
    return texts


def _normalize_embedding(embedding: Sequence[Any]) -> List[float]:
    return [float(value) for value in embedding]


def _normalize_usage(usage: Optional[Dict[str, Any]]) -> Dict[str, int]:
    if not usage:
        return {}
    normalized: Dict[str, int] = {}
    for key in ("prompt_tokens", "total_tokens"):
        if key in usage and usage[key] is not None:
            normalized[key] = int(usage[key])
    return normalized


@dataclass(frozen=True)
class EmbeddingsRequest:
    input: Any
    model: str = DEFAULT_MODEL
    dimensions: Optional[int] = None

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"input": _coerce_text_input(self.input), "model": self.model}
        if self.dimensions is not None:
            payload["dimensions"] = int(self.dimensions)
        return payload


@dataclass(frozen=True)
class EmbeddingItem:
    index: int
    embedding: List[float]
    object: str = "embedding"

    @classmethod
    def from_api(cls, data: Dict[str, Any]) -> "EmbeddingItem":
        return cls(index=int(data["index"]), embedding=_normalize_embedding(data["embedding"]), object=str(data.get("object", "embedding")))


@dataclass(frozen=True)
class EmbeddingsResponse:
    data: List[EmbeddingItem] = field(default_factory=list)
    model: Optional[str] = None
    object: str = "list"
    usage: Dict[str, int] = field(default_factory=dict)

    @classmethod
    def from_api(cls, payload: Dict[str, Any]) -> "EmbeddingsResponse":
        return cls(
            data=[EmbeddingItem.from_api(item) for item in payload.get("data", [])],
            model=payload.get("model"),
            object=str(payload.get("object", "list")),
            usage=_normalize_usage(payload.get("usage")),
        )

    def to_embeddings(self) -> List[List[float]]:
        return [item.embedding for item in self.data]
