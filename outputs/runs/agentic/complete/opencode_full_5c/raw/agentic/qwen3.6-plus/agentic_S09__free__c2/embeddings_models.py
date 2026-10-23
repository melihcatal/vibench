import math
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class EmbeddingRequest:
    texts: List[str]
    model: str = "text-embedding-3-small"
    dimensions: Optional[int] = None
    encoding_format: str = "float"

    def to_payload(self):
        payload = {
            "model": self.model,
            "input": self.texts,
            "encoding_format": self.encoding_format,
        }
        if self.dimensions is not None:
            payload["dimensions"] = self.dimensions
        return payload


@dataclass
class EmbeddingResponse:
    embeddings: List[List[float]]
    model: str
    usage: dict = field(default_factory=dict)
    raw_response: Optional[dict] = None

    @classmethod
    def from_openai_response(cls, response):
        embeddings = [data["embedding"] for data in response.data]
        usage = {
            "prompt_tokens": response.usage.prompt_tokens,
            "total_tokens": response.usage.total_tokens,
        }
        return cls(
            embeddings=embeddings,
            model=response.model,
            usage=usage,
            raw_response={"id": response.id, "object": response.object},
        )

    def get_embedding(self, index=0):
        return self.embeddings[index]

    def num_embeddings(self):
        return len(self.embeddings)

    def embedding_dimension(self):
        if self.embeddings:
            return len(self.embeddings[0])
        return 0


@dataclass
class SimilarityResult:
    score: float
    vector_a_norm: float
    vector_b_norm: float
    dot_product: float


def normalize_vector(vector):
    magnitude = math.sqrt(sum(x * x for x in vector))
    if magnitude == 0:
        return vector
    return [x / magnitude for x in vector]


def cosine_similarity(vec_a, vec_b):
    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must have the same dimension")
    norm_a = math.sqrt(sum(x * x for x in vec_a))
    norm_b = math.sqrt(sum(x * x for x in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    return dot / (norm_a * norm_b)


def l2_normalize_vector(vector):
    magnitude = math.sqrt(sum(x * x for x in vector))
    if magnitude == 0:
        return vector, 0.0
    return [x / magnitude for x in vector], magnitude


def batch_cosine_similarities(query_vec, doc_vecs):
    return [cosine_similarity(query_vec, dv) for dv in doc_vecs]
