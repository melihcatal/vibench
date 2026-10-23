from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class EmbeddingsRequest:
    input: str | Sequence[str]
    model: str
    user: str | None = None
    encoding_format: str | None = None
    dimensions: int | None = None
    extra: Mapping[str, Any] = field(default_factory=dict)

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "input": self.input,
            "model": self.model,
        }
        if self.user is not None:
            payload["user"] = self.user
        if self.encoding_format is not None:
            payload["encoding_format"] = self.encoding_format
        if self.dimensions is not None:
            payload["dimensions"] = self.dimensions
        if self.extra:
            payload.update(dict(self.extra))
        return payload


@dataclass(frozen=True)
class EmbeddingDatum:
    embedding: list[float]
    index: int
    object: str | None = None


@dataclass(frozen=True)
class EmbeddingsResponse:
    data: list[EmbeddingDatum]
    model: str
    object: str
    usage: Mapping[str, Any] | None = None

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "EmbeddingsResponse":
        data = [
            EmbeddingDatum(
                embedding=list(item["embedding"]),
                index=int(item["index"]),
                object=item.get("object"),
            )
            for item in payload.get("data", [])
        ]
        return cls(
            data=data,
            model=str(payload.get("model", "")),
            object=str(payload.get("object", "")),
            usage=payload.get("usage"),
        )


def normalize_embedding_vector(vector: Sequence[Any]) -> list[float]:
    return [float(value) for value in vector]


def normalize_embeddings_response(payload: Mapping[str, Any]) -> EmbeddingsResponse:
    normalized = dict(payload)
    data = []
    for item in normalized.get("data", []):
        data.append(
            {
                **dict(item),
                "embedding": normalize_embedding_vector(item.get("embedding", [])),
                "index": int(item.get("index", 0)),
            }
        )
    normalized["data"] = data
    return EmbeddingsResponse.from_payload(normalized)
