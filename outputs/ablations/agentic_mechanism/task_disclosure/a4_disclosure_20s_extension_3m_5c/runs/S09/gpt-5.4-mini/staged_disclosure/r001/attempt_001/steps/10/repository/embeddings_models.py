from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping, Sequence


@dataclass(frozen=True)
class EmbeddingsRequest:
    model: str
    input: str | Sequence[str] | Sequence[Sequence[int]]
    encoding_format: str | None = None
    user: str | None = None
    dimensions: int | None = None
    extra_body: Mapping[str, Any] = field(default_factory=dict)

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"model": self.model, "input": self.input}
        if self.encoding_format is not None:
            payload["encoding_format"] = self.encoding_format
        if self.user is not None:
            payload["user"] = self.user
        if self.dimensions is not None:
            payload["dimensions"] = self.dimensions
        payload.update(dict(self.extra_body))
        return payload


@dataclass(frozen=True)
class EmbeddingsData:
    index: int
    embedding: list[float]
    object: str | None = None


@dataclass(frozen=True)
class EmbeddingsResponse:
    object: str
    model: str
    data: list[EmbeddingsData]
    usage: dict[str, Any] | None = None


def _normalize_embedding(value: Any) -> list[float]:
    if value is None:
        return []
    if isinstance(value, list):
        return [float(v) for v in value]
    if isinstance(value, tuple):
        return [float(v) for v in value]
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [float(v) for v in value]
    raise TypeError(f"Unsupported embedding type: {type(value)!r}")


def normalize_embeddings_response(raw: Mapping[str, Any]) -> EmbeddingsResponse:
    data_items: list[EmbeddingsData] = []
    for item in raw.get("data", []) or []:
        if not isinstance(item, Mapping):
            continue
        data_items.append(
            EmbeddingsData(
                index=int(item.get("index", 0)),
                embedding=_normalize_embedding(item.get("embedding")),
                object=item.get("object"),
            )
        )
    return EmbeddingsResponse(
        object=str(raw.get("object", "list")),
        model=str(raw.get("model", "")),
        data=data_items,
        usage=dict(raw["usage"]) if isinstance(raw.get("usage"), Mapping) else None,
    )


def normalize_embeddings_input(value: Any) -> str | list[str] | list[list[int]]:
    if isinstance(value, str):
        return value
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        if all(isinstance(item, str) for item in value):
            return [str(item) for item in value]
        if all(isinstance(item, Sequence) and not isinstance(item, (str, bytes, bytearray)) for item in value):
            return [[int(v) for v in item] for item in value]
    raise TypeError("input must be a string, list of strings, or list of token sequences")
