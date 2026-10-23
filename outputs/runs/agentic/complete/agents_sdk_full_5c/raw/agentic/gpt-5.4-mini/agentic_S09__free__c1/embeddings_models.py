from dataclasses import dataclass
from typing import Any, Iterable, List


@dataclass(frozen=True)
class EmbeddingRequest:
    texts: List[str]
    model: str


@dataclass(frozen=True)
class EmbeddingResponse:
    embeddings: List[List[float]]
    model: str | None = None


def normalize_embedding_response(response: Any) -> EmbeddingResponse:
    data = sorted(response.data, key=lambda item: item.index)
    embeddings = [list(item.embedding) for item in data]
    model = getattr(response, "model", None)
    return EmbeddingResponse(embeddings=embeddings, model=model)


def normalize_texts(texts: Iterable[str]) -> List[str]:
    return [str(text).strip() for text in texts if str(text).strip()]
