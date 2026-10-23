from dataclasses import dataclass
from typing import Any, Iterable, List, Mapping, Optional, Sequence

DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


def _to_list_of_strings(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    return [str(item) for item in value]


def _to_list_of_floats(value: Any) -> List[float]:
    if value is None:
        return []
    return [float(item) for item in value]


@dataclass(frozen=True)
class EmbeddingRequest:
    model: str = DEFAULT_EMBEDDING_MODEL
    input: Sequence[str] = ()
    encoding_format: Optional[str] = None
    user: Optional[str] = None
    dimensions: Optional[int] = None

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"model": self.model, "input": list(self.input)}
        if self.encoding_format is not None:
            payload["encoding_format"] = self.encoding_format
        if self.user is not None:
            payload["user"] = self.user
        if self.dimensions is not None:
            payload["dimensions"] = self.dimensions
        return payload


@dataclass(frozen=True)
class EmbeddingData:
    index: int
    embedding: List[float]
    object: str = "embedding"

    @classmethod
    def from_api(cls, item: Mapping[str, Any]) -> "EmbeddingData":
        return cls(
            index=int(item.get("index", 0)),
            embedding=_to_list_of_floats(item.get("embedding")),
            object=str(item.get("object", "embedding")),
        )


@dataclass(frozen=True)
class EmbeddingResponse:
    data: List[EmbeddingData]
    model: str
    object: str = "list"
    usage: Optional[Mapping[str, Any]] = None

    @classmethod
    def from_api(cls, response: Any) -> "EmbeddingResponse":
        raw_data = getattr(response, "data", None)
        if raw_data is None and isinstance(response, Mapping):
            raw_data = response.get("data", [])
        items = [
            EmbeddingData.from_api(item if isinstance(item, Mapping) else item.model_dump())
            for item in (raw_data or [])
        ]
        model = getattr(response, "model", None)
        if model is None and isinstance(response, Mapping):
            model = response.get("model", DEFAULT_EMBEDDING_MODEL)
        object_name = getattr(response, "object", None)
        if object_name is None and isinstance(response, Mapping):
            object_name = response.get("object", "list")
        usage = getattr(response, "usage", None)
        if usage is None and isinstance(response, Mapping):
            usage = response.get("usage")
        return cls(data=items, model=str(model or DEFAULT_EMBEDDING_MODEL), object=str(object_name or "list"), usage=usage)


def normalize_embedding(value: Any) -> List[float]:
    if hasattr(value, "embedding"):
        value = getattr(value, "embedding")
    return _to_list_of_floats(value)


def normalize_embeddings(value: Any) -> List[List[float]]:
    if value is None:
        return []
    if hasattr(value, "data"):
        value = getattr(value, "data")
    return [normalize_embedding(item) for item in value]


def normalize_embedding_response(value: Any) -> EmbeddingResponse:
    if isinstance(value, EmbeddingResponse):
        return value
    return EmbeddingResponse.from_api(value)
