from dataclasses import dataclass
from math import sqrt


@dataclass
class EmbeddingRequest:
    input_texts: list


@dataclass
class EmbeddingResponse:
    embeddings: list


def normalize_embedding(values):
    magnitude = sqrt(sum(float(v) * float(v) for v in values))
    if magnitude == 0:
        return [0.0 for _ in values]
    return [float(v) / magnitude for v in values]


def cosine_similarity(left, right):
    left_n = normalize_embedding(left)
    right_n = normalize_embedding(right)
    return sum(a * b for a, b in zip(left_n, right_n))
