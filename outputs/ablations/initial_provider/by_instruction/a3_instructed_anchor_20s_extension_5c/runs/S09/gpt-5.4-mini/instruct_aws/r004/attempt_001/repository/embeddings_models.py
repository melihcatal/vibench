import math
from dataclasses import dataclass
from typing import Iterable, List, Sequence


def normalize_vector(vector: Sequence[float]) -> List[float]:
    norm = math.sqrt(sum(v * v for v in vector))
    if norm == 0:
        return [0.0 for _ in vector]
    return [float(v) / norm for v in vector]


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right):
        raise ValueError("Vector lengths must match")
    left_n = normalize_vector(left)
    right_n = normalize_vector(right)
    return sum(a * b for a, b in zip(left_n, right_n))


@dataclass(frozen=True)
class TextEmbeddingRequest:
    text: str


@dataclass(frozen=True)
class BatchEmbeddingRequest:
    texts: List[str]


def extract_embedding(payload):
    if isinstance(payload, dict):
        if "embedding" in payload:
            return payload["embedding"]
        if "embeddings" in payload and payload["embeddings"]:
            return payload["embeddings"][0]
    raise ValueError("Embedding response missing embedding data")


def extract_embeddings(payload):
    if isinstance(payload, dict) and "embeddings" in payload:
        return payload["embeddings"]
    if isinstance(payload, dict) and "embedding" in payload:
        return [payload["embedding"]]
    raise ValueError("Embedding response missing embeddings data")
