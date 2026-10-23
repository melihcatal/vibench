from dataclasses import dataclass
from math import sqrt
from typing import Iterable, List, Sequence


@dataclass
class EmbeddingResult:
    text: str
    vector: List[float]


def normalize_vector(vector: Sequence[float]) -> List[float]:
    norm = sqrt(sum(value * value for value in vector))
    if not norm:
        return [float(value) for value in vector]
    return [float(value) / norm for value in vector]


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    left_norm = normalize_vector(left)
    right_norm = normalize_vector(right)
    return sum(a * b for a, b in zip(left_norm, right_norm))


def extract_embeddings(response: object) -> List[List[float]]:
    return [item.embedding for item in response.data]


def batch_results(
    texts: Iterable[str], embeddings: Iterable[Sequence[float]]
) -> List[EmbeddingResult]:
    return [
        EmbeddingResult(text=text, vector=list(vec))
        for text, vec in zip(texts, embeddings)
    ]
