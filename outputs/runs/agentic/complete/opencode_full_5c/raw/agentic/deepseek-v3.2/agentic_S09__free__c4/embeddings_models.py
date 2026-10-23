from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import numpy as np


@dataclass
class EmbeddingRequest:
    """Request model for embedding operations."""

    text: str
    model: str = "text-embedding-3-small"
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class BatchEmbeddingRequest:
    """Request model for batch embedding operations."""

    texts: List[str]
    model: str = "text-embedding-3-small"
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class EmbeddingResponse:
    """Response model for embedding operations."""

    embedding: List[float]
    model: str
    text: str
    dimensions: int
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class BatchEmbeddingResponse:
    """Response model for batch embedding operations."""

    embeddings: List[List[float]]
    model: str
    texts: List[str]
    dimensions: int
    metadata: Optional[Dict[str, Any]] = None


def normalize_embedding(embedding: List[float]) -> List[float]:
    """
    Normalize an embedding vector to unit length.

    Args:
        embedding: Raw embedding vector

    Returns:
        Normalized embedding vector
    """
    vec = np.array(embedding)
    norm = np.linalg.norm(vec)
    if norm == 0:
        return embedding
    normalized = vec / norm
    return normalized.tolist()


def normalize_batch_embeddings(embeddings: List[List[float]]) -> List[List[float]]:
    """
    Normalize a batch of embedding vectors to unit length.

    Args:
        embeddings: List of raw embedding vectors

    Returns:
        List of normalized embedding vectors
    """
    return [normalize_embedding(emb) for emb in embeddings]


def cosine_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """
    Compute cosine similarity between two embedding vectors.

    Args:
        embedding1: First embedding vector
        embedding2: Second embedding vector

    Returns:
        Cosine similarity score between -1 and 1
    """
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)

    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    similarity = dot_product / (norm1 * norm2)
    return float(similarity)


def parse_openai_response(response_data: Dict[str, Any]) -> EmbeddingResponse:
    """
    Parse OpenAI API response into standardized format.

    Args:
        response_data: Raw response from OpenAI embeddings API

    Returns:
        Standardized EmbeddingResponse
    """
    embedding = response_data["data"][0]["embedding"]
    model = response_data["model"]

    return EmbeddingResponse(
        embedding=embedding,
        model=model,
        text="",  # Text not included in OpenAI response
        dimensions=len(embedding),
        metadata={
            "object": response_data.get("object"),
            "usage": response_data.get("usage"),
        },
    )
