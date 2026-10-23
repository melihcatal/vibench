import math
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class EmbeddingRequest:
    texts: List[str]
    model: str = "text-embedding-3-small"
    dimensions: Optional[int] = None


@dataclass
class EmbeddingResult:
    text: str
    embedding: List[float]
    index: int = 0


@dataclass
class EmbeddingResponse:
    results: List[EmbeddingResult]
    model: str = ""
    usage: dict = field(default_factory=dict)


def normalize_vector(vector: List[float]) -> List[float]:
    magnitude = math.sqrt(sum(x * x for x in vector))
    if magnitude == 0:
        return vector
    return [x / magnitude for x in vector]


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must have the same dimension")
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = math.sqrt(sum(x * x for x in vec_a))
    mag_b = math.sqrt(sum(x * x for x in vec_b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot_product / (mag_a * mag_b)


def build_search_results(query_embedding, doc_embeddings, doc_texts):
    results = []
    for i, doc_emb in enumerate(doc_embeddings):
        score = cosine_similarity(query_embedding, doc_emb)
        results.append({"text": doc_texts[i], "score": score, "index": i})
    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def truncate_embedding(embedding: List[float], target_dim: int) -> List[float]:
    if len(embedding) <= target_dim:
        return embedding
    return embedding[:target_dim]
