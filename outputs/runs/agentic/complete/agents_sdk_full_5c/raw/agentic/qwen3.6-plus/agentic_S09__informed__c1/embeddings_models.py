"""Local request, response, and normalization helpers for Direct Embeddings API.

Defines data classes and utility functions for working with OpenAI embeddings.
"""

import math
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict


@dataclass
class EmbeddingRequest:
    """Request payload for an embedding operation."""

    texts: List[str]
    model: str = "text-embedding-3-small"
    dimensions: Optional[int] = None
    encoding_format: str = "float"

    def to_api_params(self) -> dict:
        """Convert to OpenAI API parameters."""
        params: dict = {
            "input": self.texts,
            "model": self.model,
        }
        if self.dimensions is not None:
            params["dimensions"] = self.dimensions
        return params


@dataclass
class EmbeddingResponse:
    """Response wrapper for embedding results."""

    embeddings: List[List[float]]
    model: str
    usage: Dict[str, int] = field(default_factory=dict)
    original_texts: List[str] = field(default_factory=list)

    def get_embedding(self, index: int) -> List[float]:
        """Get embedding vector by index."""
        return self.embeddings[index]

    def text_embedding_pairs(self) -> List[Tuple[str, List[float]]]:
        """Return paired (text, embedding) tuples."""
        return list(zip(self.original_texts, self.embeddings))


@dataclass
class SimilarityResult:
    """Result of a similarity computation."""

    score: float
    text_a: str
    text_b: str


def normalize_vector(vector: List[float]) -> List[float]:
    """L2-normalize a vector.

    Args:
        vector: Raw embedding vector.

    Returns:
        L2-normalized vector.
    """
    magnitude = math.sqrt(sum(x * x for x in vector))
    if magnitude == 0:
        return [0.0] * len(vector)
    return [x / magnitude for x in vector]


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Compute cosine similarity between two vectors.

    Args:
        vec_a: First embedding vector.
        vec_b: Second embedding vector.

    Returns:
        Cosine similarity score in [-1, 1].
    """
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = math.sqrt(sum(x * x for x in vec_a))
    mag_b = math.sqrt(sum(x * x for x in vec_b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot_product / (mag_a * mag_b)


def build_similarity_result(
    text_a: str, text_b: str, vec_a: List[float], vec_b: List[float]
) -> SimilarityResult:
    """Build a SimilarityResult from two texts and their embeddings.

    Args:
        text_a: First text string.
        text_b: Second text string.
        vec_a: Embedding for text_a.
        vec_b: Embedding for text_b.

    Returns:
        SimilarityResult with computed cosine similarity.
    """
    score = cosine_similarity(vec_a, vec_b)
    return SimilarityResult(score=score, text_a=text_a, text_b=text_b)


def rank_by_similarity(
    query_embedding: List[float],
    document_embeddings: List[List[float]],
    documents: List[str],
    top_k: int = 5,
) -> List[Tuple[str, float]]:
    """Rank documents by cosine similarity to a query embedding.

    Args:
        query_embedding: Query embedding vector.
        document_embeddings: List of document embedding vectors.
        documents: List of document texts corresponding to embeddings.
        top_k: Number of top results to return.

    Returns:
        List of (document, similarity_score) tuples ranked by score descending.
    """
    scored = []
    for doc_text, doc_emb in zip(documents, document_embeddings):
        score = cosine_similarity(query_embedding, doc_emb)
        scored.append((doc_text, score))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]
