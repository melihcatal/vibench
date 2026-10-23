import math
from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict


@dataclass
class EmbeddingRequest:
    text: str
    model: str = "text-embedding-3-small"
    dimensions: Optional[int] = None

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"input": self.text, "model": self.model}
        if self.dimensions is not None:
            payload["dimensions"] = self.dimensions
        return payload


@dataclass
class BatchEmbeddingRequest:
    texts: List[str]
    model: str = "text-embedding-3-small"
    dimensions: Optional[int] = None

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"input": self.texts, "model": self.model}
        if self.dimensions is not None:
            payload["dimensions"] = self.dimensions
        return payload


@dataclass
class EmbeddingResult:
    vector: List[float]
    index: int = 0
    model: str = ""
    usage: Optional[Dict[str, int]] = None


@dataclass
class BatchEmbeddingResult:
    results: List[EmbeddingResult] = field(default_factory=list)
    model: str = ""
    usage: Optional[Dict[str, int]] = None

    def get_vectors(self) -> List[List[float]]:
        return [r.vector for r in self.results]

    def get_vector(self, index: int) -> List[float]:
        return self.results[index].vector


def normalize_vector(vector: List[float]) -> List[float]:
    magnitude = math.sqrt(sum(x * x for x in vector))
    if magnitude == 0:
        return vector
    return [x / magnitude for x in vector]


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must have the same dimension")
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(x * x for x in vec_a))
    norm_b = math.sqrt(sum(x * x for x in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def parse_openai_response_to_results(response, model: str = "") -> BatchEmbeddingResult:
    results = []
    for item in response.data:
        results.append(
            EmbeddingResult(
                vector=item.embedding,
                index=item.index,
                model=model or response.model,
            )
        )
    usage = None
    if hasattr(response, "usage"):
        usage = {
            "prompt_tokens": response.usage.prompt_tokens,
            "total_tokens": response.usage.total_tokens,
        }
    return BatchEmbeddingResult(
        results=sorted(results, key=lambda r: r.index),
        model=model or response.model,
        usage=usage,
    )
