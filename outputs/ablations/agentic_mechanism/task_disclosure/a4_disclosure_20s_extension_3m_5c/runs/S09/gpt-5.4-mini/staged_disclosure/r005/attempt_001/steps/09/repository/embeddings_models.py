from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple, Union


def _coerce_input(value: Union[str, Sequence[str]]) -> Union[str, List[str]]:
    if isinstance(value, str):
        return value
    return [str(item) for item in value]


def _coerce_float_list(values: Any) -> List[float]:
    if values is None:
        return []
    return [float(v) for v in values]


def _coerce_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    return int(value)


@dataclass
class DirectEmbeddingsRequest:
    model: str
    input: Union[str, List[str]]
    encoding_format: Optional[str] = None
    dimensions: Optional[int] = None
    user: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"model": self.model, "input": _coerce_input(self.input)}
        if self.encoding_format is not None:
            payload["encoding_format"] = self.encoding_format
        if self.dimensions is not None:
            payload["dimensions"] = int(self.dimensions)
        if self.user is not None:
            payload["user"] = self.user
        payload.update(self.extra)
        return payload


@dataclass
class DirectEmbeddingData:
    index: int
    embedding: List[float]
    object: str = "embedding"

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "DirectEmbeddingData":
        return cls(index=int(data["index"]), embedding=_coerce_float_list(data.get("embedding")), object=str(data.get("object", "embedding")))


@dataclass
class DirectEmbeddingsResponse:
    object: str
    data: List[DirectEmbeddingData]
    model: str
    usage: Dict[str, Any] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, response: Mapping[str, Any]) -> "DirectEmbeddingsResponse":
        data = [DirectEmbeddingData.from_dict(item) for item in response.get("data", [])]
        usage = dict(response.get("usage", {}) or {})
        return cls(object=str(response.get("object", "list")), data=data, model=str(response.get("model", "")), usage=usage, raw=dict(response))

    def vectors(self) -> List[List[float]]:
        return [item.embedding for item in self.data]

    def first_vector(self) -> List[float]:
        return self.data[0].embedding if self.data else []


def normalize_embeddings_request(payload: Mapping[str, Any]) -> Dict[str, Any]:
    normalized = dict(payload)
    if "input" in normalized:
        normalized["input"] = _coerce_input(normalized["input"])
    if "dimensions" in normalized and normalized["dimensions"] is not None:
        normalized["dimensions"] = int(normalized["dimensions"])
    return normalized


def normalize_embeddings_response(response: Mapping[str, Any]) -> DirectEmbeddingsResponse:
    return DirectEmbeddingsResponse.from_dict(response)
