from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence


@dataclass(frozen=True)
class EmbeddingRequest:
    model: str
    input: Sequence[str]
    encoding_format: Optional[str] = None
    dimensions: Optional[int] = None
    user: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"model": self.model, "input": list(self.input)}
        if self.encoding_format is not None:
            payload["encoding_format"] = self.encoding_format
        if self.dimensions is not None:
            payload["dimensions"] = self.dimensions
        if self.user is not None:
            payload["user"] = self.user
        return payload


@dataclass(frozen=True)
class EmbeddingItem:
    index: int
    embedding: List[float]


@dataclass(frozen=True)
class EmbeddingResponse:
    model: str
    embeddings: List[EmbeddingItem] = field(default_factory=list)

    @classmethod
    def from_api_response(cls, response: Any) -> "EmbeddingResponse":
        model = getattr(response, "model", "")
        items: List[EmbeddingItem] = []
        for item in getattr(response, "data", []) or []:
            items.append(EmbeddingItem(index=item.index, embedding=list(item.embedding)))
        return cls(model=model, embeddings=items)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model": self.model,
            "embeddings": [{"index": item.index, "embedding": item.embedding} for item in self.embeddings],
        }


def normalize_embedding(embedding: Sequence[float]) -> List[float]:
    values = [float(value) for value in embedding]
    norm = sum(value * value for value in values) ** 0.5
    if norm == 0:
        return values
    return [value / norm for value in values]


def normalize_embeddings(embeddings: Sequence[Sequence[float]]) -> List[List[float]]:
    return [normalize_embedding(embedding) for embedding in embeddings]
