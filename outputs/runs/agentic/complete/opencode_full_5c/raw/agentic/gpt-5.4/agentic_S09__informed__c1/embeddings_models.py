from dataclasses import dataclass
from typing import Any, Iterable, List, Sequence


@dataclass
class EmbeddingRequest:
    texts: List[str]
    input_type: str = "search_document"
    truncate: str = "END"


@dataclass
class EmbeddingResult:
    text: str
    embedding: List[float]
    index: int


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def normalize_texts(values: Sequence[Any] | Iterable[Any]) -> List[str]:
    normalized = [normalize_text(value) for value in values]
    return [value for value in normalized if value]


def ensure_single_text(value: Any) -> str:
    text = normalize_text(value)
    if not text:
        raise ValueError("text must be a non-empty string")
    return text


def parse_embed_response(texts: Sequence[str], response: Any) -> List[EmbeddingResult]:
    embeddings = response.embeddings or []
    return [
        EmbeddingResult(text=texts[index], embedding=list(item.embedding), index=index)
        for index, item in enumerate(embeddings)
    ]


def l2_normalize(vector: Sequence[float]) -> List[float]:
    magnitude = sum(component * component for component in vector) ** 0.5
    if magnitude == 0:
        return [0.0 for _ in vector]
    return [float(component) / magnitude for component in vector]


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right):
        raise ValueError("vectors must have the same dimensionality")
    left_norm = l2_normalize(left)
    right_norm = l2_normalize(right)
    return float(sum(a * b for a, b in zip(left_norm, right_norm)))
