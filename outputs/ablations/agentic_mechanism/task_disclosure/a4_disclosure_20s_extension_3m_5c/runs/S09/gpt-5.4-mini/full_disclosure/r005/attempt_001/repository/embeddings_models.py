from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence


@dataclass(frozen=True)
class EmbeddingRequest:
    model: str
    input: str | Sequence[str]
    dimensions: int | None = None
    user: str | None = None

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"model": self.model, "input": self.input}
        if self.dimensions is not None:
            payload["dimensions"] = self.dimensions
        if self.user is not None:
            payload["user"] = self.user
        return payload


@dataclass(frozen=True)
class EmbeddingData:
    index: int
    embedding: list[float]
    object: str | None = None


@dataclass(frozen=True)
class EmbeddingResponse:
    data: list[EmbeddingData]
    model: str | None = None
    usage: Mapping[str, Any] | None = None
    object: str | None = None

    @classmethod
    def from_api_response(cls, payload: Mapping[str, Any]) -> "EmbeddingResponse":
        data = [
            EmbeddingData(
                index=int(item["index"]),
                embedding=[float(v) for v in item["embedding"]],
                object=item.get("object"),
            )
            for item in payload.get("data", [])
        ]
        return cls(
            data=data,
            model=payload.get("model"),
            usage=payload.get("usage"),
            object=payload.get("object"),
        )


def normalize_embedding(values: Iterable[Any]) -> list[float]:
    vector = [float(value) for value in values]
    norm = sum(component * component for component in vector) ** 0.5
    if norm == 0:
        return vector
    return [component / norm for component in vector]


def extract_embedding(response: Mapping[str, Any] | EmbeddingResponse) -> list[float]:
    if isinstance(response, EmbeddingResponse):
        if not response.data:
            return []
        return list(response.data[0].embedding)
    data = response.get("data", [])
    if not data:
        return []
    return [float(v) for v in data[0]["embedding"]]


def extract_embeddings(response: Mapping[str, Any] | EmbeddingResponse) -> list[list[float]]:
    if isinstance(response, EmbeddingResponse):
        return [list(item.embedding) for item in response.data]
    return [[float(v) for v in item["embedding"]] for item in response.get("data", [])]
