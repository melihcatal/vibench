import math
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class EmbeddingRequest:
    input: str | List[str]
    model: str = "text-embedding-3-small"
    encoding_format: str = "float"
    dimensions: Optional[int] = None


@dataclass
class SingleEmbeddingResponse:
    embedding: List[float]
    index: int
    object_type: str = "embedding"


@dataclass
class BatchEmbeddingResponse:
    data: List[SingleEmbeddingResponse] = field(default_factory=list)
    model: str = ""
    usage: Optional[dict] = None


@dataclass
class EmbeddingJobSummary:
    total_texts: int = 0
    total_tokens: int = 0
    embedding_dimension: int = 0
    model: str = ""
    average_norm: float = 0.0
    errors: List[str] = field(default_factory=list)


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


def build_embedding_request(
    text: str, model: str, dimensions: Optional[int] = None
) -> dict:
    payload = {
        "input": text,
        "model": model,
        "encoding_format": "float",
    }
    if dimensions is not None:
        payload["dimensions"] = dimensions
    return payload


def build_batch_embedding_request(
    texts: List[str], model: str, dimensions: Optional[int] = None
) -> dict:
    payload = {
        "input": texts,
        "model": model,
        "encoding_format": "float",
    }
    if dimensions is not None:
        payload["dimensions"] = dimensions
    return payload


def parse_single_embedding_response(api_response) -> SingleEmbeddingResponse:
    data = api_response.data[0]
    return SingleEmbeddingResponse(
        embedding=data.embedding,
        index=data.index,
        object_type=data.object,
    )


def parse_batch_embedding_response(api_response) -> BatchEmbeddingResponse:
    items = []
    for item in api_response.data:
        items.append(
            SingleEmbeddingResponse(
                embedding=item.embedding,
                index=item.index,
                object_type=item.object,
            )
        )
    return BatchEmbeddingResponse(
        data=items,
        model=api_response.model,
        usage={
            "prompt_tokens": api_response.usage.prompt_tokens,
            "total_tokens": api_response.usage.total_tokens,
        }
        if api_response.usage
        else None,
    )
