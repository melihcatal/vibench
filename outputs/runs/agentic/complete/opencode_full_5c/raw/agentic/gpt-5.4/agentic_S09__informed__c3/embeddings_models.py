from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Sequence


def normalize_text(value: str) -> str:
    text = value.strip()
    if not text:
        raise ValueError("text must not be empty")
    return text


def normalize_texts(values: Sequence[str]) -> list[str]:
    texts = [normalize_text(value) for value in values]
    if not texts:
        raise ValueError("texts must not be empty")
    return texts


def normalize_vector(values: Iterable[float]) -> list[float]:
    return [float(value) for value in values]


@dataclass(slots=True)
class EmbeddingRequest:
    texts: list[str]
    model: str
    input_type: str = "search_document"


@dataclass(slots=True)
class EmbeddingResponse:
    model: str
    embeddings: list[list[float]]
    usage: dict[str, Any]


def build_embedding_request(
    texts: Sequence[str], model: str, input_type: str = "search_document"
) -> EmbeddingRequest:
    return EmbeddingRequest(
        texts=normalize_texts(texts), model=model, input_type=input_type
    )


def parse_embedding_response(response: Any, model: str) -> EmbeddingResponse:
    embeddings = [normalize_vector(item.embedding) for item in response.embeddings]
    billed_units = getattr(response.meta, "billed_units", None)
    usage = {
        "input_tokens": getattr(billed_units, "input_tokens", None),
        "search_units": getattr(billed_units, "search_units", None),
    }
    return EmbeddingResponse(model=model, embeddings=embeddings, usage=usage)
