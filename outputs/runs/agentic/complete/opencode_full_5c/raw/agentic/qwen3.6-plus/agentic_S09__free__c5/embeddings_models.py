import os
from dataclasses import dataclass, field
from typing import List, Optional
import math


@dataclass
class EmbeddingRequest:
    model: str = "text-embedding-3-small"
    input_text: str = ""
    dimensions: Optional[int] = None
    encoding_format: str = "float"


@dataclass
class EmbeddingResponse:
    embedding: List[float]
    model: str = ""
    usage_prompt_tokens: int = 0
    input_text: str = ""


@dataclass
class BatchEmbeddingRequest:
    model: str = "text-embedding-3-small"
    input_texts: List[str] = field(default_factory=list)
    dimensions: Optional[int] = None
    encoding_format: str = "float"


@dataclass
class BatchEmbeddingResponse:
    embeddings: List[List[float]] = field(default_factory=list)
    model: str = ""
    usage_prompt_tokens: int = 0
    input_texts: List[str] = field(default_factory=list)


@dataclass
class SimilarityResult:
    text_a: str = ""
    text_b: str = ""
    similarity: float = 0.0
    embedding_a: List[float] = field(default_factory=list)
    embedding_b: List[float] = field(default_factory=list)


@dataclass
class SearchResult:
    query: str = ""
    document: str = ""
    score: float = 0.0
    rank: int = 0
    embedding: List[float] = field(default_factory=list)


@dataclass
class EmbeddingJobSummary:
    total_texts: int = 0
    total_tokens: int = 0
    model: str = ""
    dimensions: int = 0
    average_token_length: float = 0.0
    success_count: int = 0
    failed_count: int = 0


def normalize_vector(vector: List[float]) -> List[float]:
    magnitude = math.sqrt(sum(x * x for x in vector))
    if magnitude == 0:
        return vector
    return [x / magnitude for x in vector]


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = math.sqrt(sum(x * x for x in vec_a))
    magnitude_b = math.sqrt(sum(x * x for x in vec_b))
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)


def truncate_embedding(embedding: List[float], dimensions: int) -> List[float]:
    return embedding[:dimensions]


def build_openai_payload(request: EmbeddingRequest) -> dict:
    payload = {
        "model": request.model,
        "input": request.input_text,
        "encoding_format": request.encoding_format,
    }
    if request.dimensions is not None:
        payload["dimensions"] = request.dimensions
    return payload


def build_openai_batch_payload(request: BatchEmbeddingRequest) -> dict:
    payload = {
        "model": request.model,
        "input": request.input_texts,
        "encoding_format": request.encoding_format,
    }
    if request.dimensions is not None:
        payload["dimensions"] = request.dimensions
    return payload


def parse_openai_response(
    response_data: dict, input_text: str = ""
) -> EmbeddingResponse:
    embedding = response_data["data"][0]["embedding"]
    usage = response_data.get("usage", {})
    return EmbeddingResponse(
        embedding=embedding,
        model=response_data.get("model", ""),
        usage_prompt_tokens=usage.get("prompt_tokens", 0),
        input_text=input_text,
    )


def parse_openai_batch_response(
    response_data: dict, input_texts: List[str]
) -> BatchEmbeddingResponse:
    embeddings = []
    total_tokens = 0
    for item in sorted(response_data["data"], key=lambda x: x["index"]):
        embeddings.append(item["embedding"])
    usage = response_data.get("usage", {})
    total_tokens = usage.get("prompt_tokens", 0)
    return BatchEmbeddingResponse(
        embeddings=embeddings,
        model=response_data.get("model", ""),
        usage_prompt_tokens=total_tokens,
        input_texts=input_texts,
    )
