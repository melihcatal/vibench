from dataclasses import dataclass, field
from typing import Any, Iterable, List, Optional, Sequence, Union


TextInput = Union[str, Sequence[str]]
EmbeddingVector = List[float]


@dataclass
class EmbeddingsRequest:
    input: TextInput
    model: str
    encoding_format: Optional[str] = None
    dimensions: Optional[int] = None
    user: Optional[str] = None

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"input": self.input, "model": self.model}
        if self.encoding_format is not None:
            payload["encoding_format"] = self.encoding_format
        if self.dimensions is not None:
            payload["dimensions"] = self.dimensions
        if self.user is not None:
            payload["user"] = self.user
        return payload


@dataclass
class EmbeddingData:
    index: int
    embedding: EmbeddingVector
    object: str = "embedding"


@dataclass
class EmbeddingsResponse:
    data: List[EmbeddingData]
    model: str
    object: str = "list"
    usage: Optional[dict[str, Any]] = None


def normalize_embedding(value: Any) -> EmbeddingVector:
    if value is None:
        return []
    if isinstance(value, list):
        return [float(x) for x in value]
    if isinstance(value, tuple):
        return [float(x) for x in value]
    if isinstance(value, str):
        parts = [p.strip() for p in value.replace("\n", ",").split(",") if p.strip()]
        return [float(p) for p in parts]
    if isinstance(value, Iterable):
        return [float(x) for x in value]
    raise TypeError("Unsupported embedding value")


def normalize_embedding_item(item: Any) -> EmbeddingData:
    if isinstance(item, EmbeddingData):
        return item
    if isinstance(item, dict):
        return EmbeddingData(
            index=int(item.get("index", 0)),
            embedding=normalize_embedding(item.get("embedding", [])),
            object=str(item.get("object", "embedding")),
        )
    raise TypeError("Unsupported embedding item")


def normalize_embeddings_response(value: Any) -> EmbeddingsResponse:
    if isinstance(value, EmbeddingsResponse):
        return value
    if not isinstance(value, dict):
        raise TypeError("Unsupported embeddings response")
    data = [normalize_embedding_item(item) for item in value.get("data", [])]
    return EmbeddingsResponse(
        data=data,
        model=str(value.get("model", "")),
        object=str(value.get("object", "list")),
        usage=value.get("usage"),
    )
