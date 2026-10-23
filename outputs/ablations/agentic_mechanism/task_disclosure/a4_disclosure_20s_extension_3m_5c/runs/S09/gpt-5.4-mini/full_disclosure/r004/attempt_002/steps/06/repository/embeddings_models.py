import os
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence


DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


@dataclass(frozen=True)
class EmbeddingRequest:
    model: str = DEFAULT_EMBEDDING_MODEL
    input: Any = field(default_factory=list)
    encoding_format: Optional[str] = None
    user: Optional[str] = None
    dimensions: Optional[int] = None

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"model": self.model, "input": self.input}
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
    def from_dict(cls, data: Mapping[str, Any]) -> "EmbeddingData":
        return cls(index=int(data["index"]), embedding=list(data["embedding"]), object=str(data.get("object", "embedding")))


@dataclass(frozen=True)
class EmbeddingResponse:
    data: List[EmbeddingData]
    model: str
    object: str
    usage: Dict[str, Any]

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "EmbeddingResponse":
        data = [EmbeddingData.from_dict(item) for item in payload.get("data", [])]
        data.sort(key=lambda item: item.index)
        return cls(data=data, model=str(payload.get("model", "")), object=str(payload.get("object", "")), usage=dict(payload.get("usage", {})))


def normalize_embedding(embedding: Sequence[float]) -> List[float]:
    values = [float(value) for value in embedding]
    norm = sum(value * value for value in values) ** 0.5
    if norm == 0.0:
        return values
    return [value / norm for value in values]


def normalize_embeddings(embeddings: Iterable[Sequence[float]]) -> List[List[float]]:
    return [normalize_embedding(embedding) for embedding in embeddings]


def extract_embeddings(payload: Mapping[str, Any]) -> List[List[float]]:
    response = EmbeddingResponse.from_dict(payload)
    return [item.embedding for item in response.data]
