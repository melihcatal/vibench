import math
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class EmbeddingRequest:
    input: str | List[str]
    model: str = "text-embedding-3-small"
    dimensions: Optional[int] = None

    def to_openai_kwargs(self) -> Dict[str, Any]:
        kwargs = {
            "model": self.model,
            "input": self.input if isinstance(self.input, list) else [self.input],
        }
        if self.dimensions:
            kwargs["dimensions"] = self.dimensions
        return kwargs


@dataclass
class EmbeddingResponse:
    embeddings: List[List[float]]
    model: str
    usage: Dict[str, int] = field(default_factory=dict)

    @classmethod
    def from_openai_response(cls, response) -> "EmbeddingResponse":
        return cls(
            embeddings=[item.embedding for item in response.data],
            model=response.model,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "total_tokens": response.usage.total_tokens,
            },
        )


def l2_normalize(vector: List[float]) -> List[float]:
    magnitude = math.sqrt(sum(v * v for v in vector))
    if magnitude == 0:
        return vector
    return [v / magnitude for v in vector]


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = math.sqrt(sum(a * a for a in vec_a))
    mag_b = math.sqrt(sum(b * b for b in vec_b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def rank_documents_by_similarity(
    query_embedding: List[float],
    doc_embeddings: List[List[float]],
    documents: List[str],
    top_k: Optional[int] = None,
) -> List[Dict[str, Any]]:
    results = []
    for i, doc_emb in enumerate(doc_embeddings):
        score = cosine_similarity(query_embedding, doc_emb)
        results.append(
            {
                "document": documents[i],
                "similarity": score,
                "index": i,
            }
        )
    results.sort(key=lambda x: x["similarity"], reverse=True)
    if top_k:
        results = results[:top_k]
    return results
