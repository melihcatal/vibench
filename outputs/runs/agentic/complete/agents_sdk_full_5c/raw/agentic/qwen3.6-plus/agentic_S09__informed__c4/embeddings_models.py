"""
Local request, response, and normalization helpers for OpenAI Embeddings API.

Defines typed helper classes and parsing utilities for embedding
requests and OpenAI API responses.
"""

from dataclasses import dataclass, field
from typing import List, Optional

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


@dataclass
class EmbeddingRequest:
    """
    Represents a single embedding request for OpenAI.

    Attributes:
        text: The input text string to embed.
        model: OpenAI model identifier, e.g. text-embedding-3-small.
        dimensions: Desired output vector dimensions (optional).
    """

    text: str
    model: str = OPENAI_EMBEDDING_MODEL
    dimensions: Optional[int] = 1536

    def to_payload(self) -> dict:
        payload = {"model": self.model, "input": self.text}
        if self.dimensions is not None:
            payload["dimensions"] = self.dimensions
        return payload


@dataclass
class EmbeddingResponse:
    """
    Parsed embedding response from OpenAI embeddings.create().

    Attributes:
        embedding: List[float] vector of embedding values.
        model: Model ID that produced the embedding.
        usage_tokens: Token count consumed for this request.
    """

    embedding: List[float] = field(default_factory=list)
    model: str = ""
    usage_tokens: int = 0


def parse_embedding_response(raw_response) -> EmbeddingResponse:
    """
    Parse an openai.types.CreateEmbeddingResponse into an EmbeddingResponse.

    Args:
        raw_response: Response object from openai_client.embeddings.create().

    Returns:
        EmbeddingResponse with extracted vector, model, and usage.
    """
    data = raw_response.data[0]
    return EmbeddingResponse(
        embedding=data.embedding,
        model=raw_response.model,
        usage_tokens=raw_response.usage.total_tokens,
    )


def parse_batch_embedding_responses(raw_response) -> List[EmbeddingResponse]:
    """
    Parse a batch OpenAI embedding response into a list of EmbeddingResponse.

    Args:
        raw_response: Response from openai_client.embeddings.create() with list input.

    Returns:
        List of EmbeddingResponse, one per input text.
    """
    results = []
    for item in raw_response.data:
        results.append(
            EmbeddingResponse(
                embedding=item.embedding,
                model=raw_response.model,
                usage_tokens=raw_response.usage.total_tokens,
            )
        )
    return results


def normalize_vector(vector: List[float]) -> List[float]:
    """
    L2-normalize an embedding vector.

    Args:
        vector: Raw embedding list of floats.

    Returns:
        L2-normalized vector.
    """
    magnitude = sum(v * v for v in vector) ** 0.5
    if magnitude == 0:
        return vector
    return [v / magnitude for v in vector]


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """
    Compute cosine similarity between two embedding vectors.

    Args:
        vec_a: First embedding vector.
        vec_b: Second embedding vector.

    Returns:
        Cosine similarity score in [-1, 1].
    """
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = sum(v * v for v in vec_a) ** 0.5
    mag_b = sum(v * v for v in vec_b) ** 0.5
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)
