from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class EmbeddingsRequest:
    model: str
    input: Sequence[str] | str
    encoding_format: str = "float"
    user: str | None = None

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"model": self.model, "input": self.input, "encoding_format": self.encoding_format}
        if self.user is not None:
            payload["user"] = self.user
        return payload


@dataclass(frozen=True)
class EmbeddingData:
    embedding: list[float]
    index: int
    object: str = "embedding"


@dataclass(frozen=True)
class EmbeddingsResponse:
    data: list[EmbeddingData]
    model: str | None = None
    object: str = "list"
    usage: Mapping[str, Any] | None = None


def _coerce_float_list(value: Any) -> list[float]:
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [float(v) for v in value]
    raise TypeError("embedding must be a sequence of numbers")


def normalize_embedding(value: Any) -> list[float]:
    return _coerce_float_list(value)


def normalize_embeddings_response(payload: Mapping[str, Any]) -> EmbeddingsResponse:
    data_items = payload.get("data", [])
    data: list[EmbeddingData] = []
    for item in data_items:
        if not isinstance(item, Mapping):
            raise TypeError("response data items must be mappings")
        data.append(
            EmbeddingData(
                embedding=normalize_embedding(item.get("embedding", [])),
                index=int(item.get("index", 0)),
                object=str(item.get("object", "embedding")),
            )
        )
    usage = payload.get("usage")
    if usage is not None and not isinstance(usage, Mapping):
        raise TypeError("usage must be a mapping if present")
    return EmbeddingsResponse(
        data=data,
        model=payload.get("model"),
        object=str(payload.get("object", "list")),
        usage=usage,
    )
