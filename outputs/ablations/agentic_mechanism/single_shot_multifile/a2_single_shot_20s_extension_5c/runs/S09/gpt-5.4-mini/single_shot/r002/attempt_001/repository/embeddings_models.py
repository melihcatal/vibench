from dataclasses import dataclass
from math import sqrt
from typing import Any, Dict, List, Sequence


@dataclass
class EmbeddingRequest:
    input: str
    model: str


@dataclass
class BatchEmbeddingRequest:
    inputs: List[str]
    model: str


def normalize_text(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    cleaned = " ".join(text.strip().split())
    if not cleaned:
        raise ValueError("text must not be empty")
    return cleaned


def normalize_texts(texts: Sequence[str]) -> List[str]:
    if not texts:
        raise ValueError("texts must not be empty")
    return [normalize_text(text) for text in texts]


def validate_embedding(embedding: List[float]) -> None:
    if not isinstance(embedding, list) or not embedding:
        raise ValueError("embedding must be a non-empty list")


def extract_single_embedding(response: Dict[str, Any]) -> List[float]:
    data = response.get("data", [])
    if not data:
        raise ValueError("embedding response missing data")
    return list(data[0]["embedding"])


def extract_embeddings(response: Dict[str, Any]) -> List[List[float]]:
    data = response.get("data", [])
    if not data:
        raise ValueError("embedding response missing data")
    return [list(item["embedding"]) for item in data]


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    validate_embedding(vec_a)
    validate_embedding(vec_b)
    if len(vec_a) != len(vec_b):
        raise ValueError("embeddings must have the same length")
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = sqrt(sum(a * a for a in vec_a))
    mag_b = sqrt(sum(b * b for b in vec_b))
    if mag_a == 0 or mag_b == 0:
        raise ValueError("embedding magnitude must be non-zero")
    return dot / (mag_a * mag_b)
