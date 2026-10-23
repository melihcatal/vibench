from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Union


EmbeddingInput = Union[str, Sequence[str], Sequence[int], Sequence[Sequence[int]]]


@dataclass
class EmbeddingsRequest:
    input: EmbeddingInput
    model: str
    dimensions: Optional[int] = None
    encoding_format: Optional[str] = None
    user: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"input": self.input, "model": self.model}
        if self.dimensions is not None:
            payload["dimensions"] = self.dimensions
        if self.encoding_format is not None:
            payload["encoding_format"] = self.encoding_format
        if self.user is not None:
            payload["user"] = self.user
        payload.update(self.extra)
        return payload


@dataclass
class EmbeddingData:
    embedding: List[float]
    index: int
    object: str = "embedding"

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "EmbeddingData":
        return cls(
            embedding=normalize_embedding(data.get("embedding", [])),
            index=int(data.get("index", 0)),
            object=str(data.get("object", "embedding")),
        )


@dataclass
class EmbeddingsResponse:
    data: List[EmbeddingData]
    model: Optional[str] = None
    object: str = "list"
    usage: Dict[str, Any] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, response: Mapping[str, Any]) -> "EmbeddingsResponse":
        data = [EmbeddingData.from_mapping(item) for item in response.get("data", [])]
        return cls(
            data=data,
            model=response.get("model"),
            object=str(response.get("object", "list")),
            usage=dict(response.get("usage", {}) or {}),
            raw=dict(response),
        )


def normalize_embedding(value: Any) -> List[float]:
    if value is None:
        return []
    if isinstance(value, list):
        return [float(item) for item in value]
    if isinstance(value, tuple):
        return [float(item) for item in value]
    if hasattr(value, "tolist"):
        return [float(item) for item in value.tolist()]
    return [float(value)]


def normalize_embeddings_response(response: Mapping[str, Any]) -> EmbeddingsResponse:
    return EmbeddingsResponse.from_mapping(response)


def build_embeddings_request(
    input: EmbeddingInput,
    model: str,
    **kwargs: Any,
) -> EmbeddingsRequest:
    extra = dict(kwargs)
    dimensions = extra.pop("dimensions", None)
    encoding_format = extra.pop("encoding_format", None)
    user = extra.pop("user", None)
    return EmbeddingsRequest(
        input=input,
        model=model,
        dimensions=dimensions,
        encoding_format=encoding_format,
        user=user,
        extra=extra,
    )
