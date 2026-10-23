from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping, Sequence


def _normalize_input(value: Any) -> str | list[str]:
    if isinstance(value, str):
        return value
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray, str)):
        return [str(item) for item in value]
    raise TypeError("input must be a string or a sequence of strings")


def _normalize_dimensions(value: Any | None) -> int | None:
    if value is None:
        return None
    dimensions = int(value)
    if dimensions <= 0:
        raise ValueError("dimensions must be greater than 0")
    return dimensions


def _normalize_encoding_format(value: Any | None) -> str | None:
    if value is None:
        return None
    encoding_format = str(value)
    if not encoding_format:
        raise ValueError("encoding_format must not be empty")
    return encoding_format


def _normalize_metadata(value: Any | None) -> dict[str, Any] | None:
    if value is None:
        return None
    if not isinstance(value, Mapping):
        raise TypeError("metadata must be a mapping")
    return dict(value)


@dataclass(slots=True)
class DirectEmbeddingsRequest:
    input: str | list[str]
    model: str
    dimensions: int | None = None
    encoding_format: str | None = None
    user: str | None = None
    metadata: dict[str, Any] | None = field(default=None)

    @classmethod
    def from_raw(cls, payload: Mapping[str, Any]) -> "DirectEmbeddingsRequest":
        return cls(
            input=_normalize_input(payload["input"]),
            model=str(payload["model"]),
            dimensions=_normalize_dimensions(payload.get("dimensions")),
            encoding_format=_normalize_encoding_format(payload.get("encoding_format")),
            user=None if payload.get("user") is None else str(payload["user"]),
            metadata=_normalize_metadata(payload.get("metadata")),
        )

    def to_dict(self) -> dict[str, Any]:
        data = {"input": self.input, "model": self.model}
        if self.dimensions is not None:
            data["dimensions"] = self.dimensions
        if self.encoding_format is not None:
            data["encoding_format"] = self.encoding_format
        if self.user is not None:
            data["user"] = self.user
        if self.metadata is not None:
            data["metadata"] = dict(self.metadata)
        return data


@dataclass(slots=True)
class EmbeddingData:
    embedding: list[float]
    index: int
    object: str = "embedding"

    @classmethod
    def from_raw(cls, payload: Mapping[str, Any]) -> "EmbeddingData":
        embedding = payload.get("embedding", [])
        if isinstance(embedding, Iterable) and not isinstance(embedding, (str, bytes, bytearray)):
            normalized_embedding = [float(item) for item in embedding]
        else:
            raise TypeError("embedding must be an iterable of numbers")
        return cls(
            embedding=normalized_embedding,
            index=int(payload["index"]),
            object=str(payload.get("object", "embedding")),
        )


@dataclass(slots=True)
class DirectEmbeddingsResponse:
    object: str
    model: str
    data: list[EmbeddingData]
    usage: dict[str, Any] | None = None

    @classmethod
    def from_raw(cls, payload: Mapping[str, Any]) -> "DirectEmbeddingsResponse":
        data = payload.get("data", [])
        if not isinstance(data, Sequence) or isinstance(data, (str, bytes, bytearray)):
            raise TypeError("data must be a sequence")
        return cls(
            object=str(payload.get("object", "list")),
            model=str(payload["model"]),
            data=[EmbeddingData.from_raw(item) for item in data],
            usage=dict(payload["usage"]) if isinstance(payload.get("usage"), Mapping) else None,
        )


def normalize_direct_embeddings_request(payload: Mapping[str, Any]) -> dict[str, Any]:
    return DirectEmbeddingsRequest.from_raw(payload).to_dict()


def normalize_direct_embeddings_response(payload: Mapping[str, Any]) -> DirectEmbeddingsResponse:
    return DirectEmbeddingsResponse.from_raw(payload)
