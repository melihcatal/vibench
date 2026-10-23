from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class EmbeddingModel(str, Enum):
    """Supported embedding models."""

    TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small"
    TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large"
    TEXT_EMBEDDING_ADA_002 = "text-embedding-ada-002"


@dataclass
class EmbeddingRequest:
    """Request model for embedding generation."""

    text: str
    model: EmbeddingModel = EmbeddingModel.TEXT_EMBEDDING_3_SMALL
    user: Optional[str] = None

    def to_openai_dict(self) -> Dict[str, Any]:
        """Convert to OpenAI API request format."""
        request = {
            "model": self.model.value,
            "input": self.text,
            "encoding_format": "float",
        }
        if self.user:
            request["user"] = self.user
        return request


@dataclass
class BatchEmbeddingRequest:
    """Request model for batch embedding generation."""

    texts: List[str]
    model: EmbeddingModel = EmbeddingModel.TEXT_EMBEDDING_3_SMALL
    user: Optional[str] = None

    def to_openai_dict(self) -> Dict[str, Any]:
        """Convert to OpenAI API request format."""
        request = {
            "model": self.model.value,
            "input": self.texts,
            "encoding_format": "float",
        }
        if self.user:
            request["user"] = self.user
        return request


@dataclass
class EmbeddingResponse:
    """Response model for embedding generation."""

    embedding: List[float]
    model: str
    text: str

    @classmethod
    def from_openai_response(
        cls, openai_response: Any, text: str
    ) -> "EmbeddingResponse":
        """Create from OpenAI API response."""
        return cls(
            embedding=openai_response.embedding, model=openai_response.model, text=text
        )


@dataclass
class BatchEmbeddingResponse:
    """Response model for batch embedding generation."""

    embeddings: List[List[float]]
    model: str
    texts: List[str]

    @classmethod
    def from_openai_response(
        cls, openai_response: Any, texts: List[str]
    ) -> "BatchEmbeddingResponse":
        """Create from OpenAI API response."""
        return cls(
            embeddings=[item.embedding for item in openai_response.data],
            model=openai_response.model,
            texts=texts,
        )


@dataclass
class SimilarityRequest:
    """Request model for similarity computation."""

    text1: str
    text2: str
    model: EmbeddingModel = EmbeddingModel.TEXT_EMBEDDING_3_SMALL


@dataclass
class SimilarityResponse:
    """Response model for similarity computation."""

    similarity: float
    model: str
    text1: str
    text2: str


@dataclass
class SearchRequest:
    """Request model for semantic search."""

    query: str
    documents: List[str]
    model: EmbeddingModel = EmbeddingModel.TEXT_EMBEDDING_3_SMALL
    top_k: Optional[int] = None


@dataclass
class SearchResult:
    """Individual search result."""

    document: str
    similarity: float
    index: int


@dataclass
class SearchResponse:
    """Response model for semantic search."""

    query_embedding: List[float]
    document_embeddings: List[List[float]]
    results: List[SearchResult]
    model: str

    def get_top_results(self, k: int = 5) -> List[SearchResult]:
        """Get top-k results by similarity."""
        sorted_results = sorted(self.results, key=lambda x: x.similarity, reverse=True)
        return sorted_results[:k]


def normalize_embedding(embedding: List[float]) -> List[float]:
    """
    Normalize embedding vector to unit length.

    Args:
        embedding: The embedding vector

    Returns:
        List[float]: Normalized embedding vector
    """
    import math

    norm = math.sqrt(sum(x * x for x in embedding))
    if norm == 0:
        return embedding
    return [x / norm for x in embedding]


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Compute cosine similarity between two vectors.

    Args:
        vec1: First vector
        vec2: Second vector

    Returns:
        float: Cosine similarity score
    """
    if len(vec1) != len(vec2):
        raise ValueError("Vectors must have the same length")

    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot_product / (norm1 * norm2)
