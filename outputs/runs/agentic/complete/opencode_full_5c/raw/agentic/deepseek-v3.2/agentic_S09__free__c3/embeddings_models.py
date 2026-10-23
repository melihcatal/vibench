from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum
import numpy as np


class EmbeddingModel(str, Enum):
    """Available OpenAI embedding models."""

    TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small"
    TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large"
    TEXT_EMBEDDING_ADA_002 = "text-embedding-ada-002"


@dataclass
class EmbeddingRequest:
    """Request model for embedding operations."""

    texts: List[str]
    model: EmbeddingModel = EmbeddingModel.TEXT_EMBEDDING_3_SMALL
    encoding_format: str = "float"
    user: Optional[str] = None

    def to_openai_format(self) -> Dict[str, Any]:
        """Convert to OpenAI API format."""
        request = {
            "model": self.model.value,
            "input": self.texts,
            "encoding_format": self.encoding_format,
        }
        if self.user:
            request["user"] = self.user
        return request


@dataclass
class EmbeddingResponse:
    """Response model for embedding operations."""

    embeddings: List[List[float]]
    model: str
    usage: Dict[str, int]

    @classmethod
    def from_openai_response(cls, openai_response: Any) -> "EmbeddingResponse":
        """Create from OpenAI API response."""
        embeddings = [item.embedding for item in openai_response.data]
        model = openai_response.model
        usage = {
            "prompt_tokens": openai_response.usage.prompt_tokens,
            "total_tokens": openai_response.usage.total_tokens,
        }
        return cls(embeddings=embeddings, model=model, usage=usage)


@dataclass
class SimilarityResult:
    """Result model for similarity calculations."""

    text1: str
    text2: str
    similarity_score: float
    embeddings1: List[float]
    embeddings2: List[float]


@dataclass
class SearchResult:
    """Result model for semantic search."""

    query: str
    documents: List[str]
    query_embedding: List[float]
    document_embeddings: List[List[float]]
    similarity_scores: List[float]
    ranked_indices: List[int]

    def get_top_k(self, k: int = 5) -> List[Dict[str, Any]]:
        """Get top K search results."""
        if k > len(self.documents):
            k = len(self.documents)

        top_results = []
        for idx in self.ranked_indices[:k]:
            top_results.append(
                {
                    "document": self.documents[idx],
                    "similarity_score": self.similarity_scores[idx],
                    "embedding": self.document_embeddings[idx],
                }
            )
        return top_results


class EmbeddingNormalizer:
    """Helper class for normalizing embeddings."""

    @staticmethod
    def normalize_vector(vector: List[float]) -> List[float]:
        """Normalize a vector to unit length."""
        vec = np.array(vector)
        norm = np.linalg.norm(vec)
        if norm == 0:
            return vector
        normalized = vec / norm
        return normalized.tolist()

    @staticmethod
    def normalize_batch(embeddings: List[List[float]]) -> List[List[float]]:
        """Normalize a batch of embeddings."""
        return [EmbeddingNormalizer.normalize_vector(vec) for vec in embeddings]

    @staticmethod
    def validate_embedding_dimension(embedding: List[float], expected_dim: int) -> bool:
        """Validate embedding dimension."""
        return len(embedding) == expected_dim

    @staticmethod
    def truncate_text(text: str, max_tokens: int = 8191) -> str:
        """
        Truncate text to fit within token limits.
        OpenAI embeddings have a limit of 8191 tokens.
        """
        # Simple character-based truncation (for demonstration)
        # In production, use a proper tokenizer
        max_chars = max_tokens * 4  # Rough estimate: 4 chars per token
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "..."
