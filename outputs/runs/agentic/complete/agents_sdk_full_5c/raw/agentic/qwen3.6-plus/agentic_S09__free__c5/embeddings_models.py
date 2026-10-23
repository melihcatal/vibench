"""
Define local request, response, and normalization helpers for Direct Embeddings API.

Provider: OpenAI Embeddings API (https://api.openai.com)
Model: text-embedding-3-small
"""

import math
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

from embeddings_client import DEFAULT_EMBEDDING_MODEL, DEFAULT_EMBEDDING_DIMENSIONS


@dataclass
class EmbeddingRequest:
    """
    Request model for OpenAI embeddings API.

    Attributes:
        texts: List of text strings to embed
        model: OpenAI model identifier (e.g., text-embedding-3-small)
        dimensions: Target embedding dimensionality
        encoding_format: Output encoding format
    """
    texts: List[str]
    model: str = DEFAULT_EMBEDDING_MODEL
    dimensions: Optional[int] = None
    encoding_format: str = "float"

    def validate(self) -> None:
        """Validate the request parameters."""
        if not self.texts:
            raise ValueError("texts list cannot be empty")
        if any(not t or not t.strip() for t in self.texts):
            raise ValueError("All text strings must be non-empty")
        if self.dimensions is not None and self.dimensions <= 0:
            raise ValueError("dimensions must be a positive integer")


@dataclass
class EmbeddingResponse:
    """
    Response model for OpenAI embeddings API.

    Attributes:
        embeddings: List of embedding vectors
        model: Model that generated the embeddings
        usage: Token usage information
    """
    embeddings: List[List[float]] = field(default_factory=list)
    model: str = ""
    usage: Dict[str, int] = field(default_factory=dict)

    @property
    def embedding_count(self) -> int:
        return len(self.embeddings)

    @property
    def dimension_count(self) -> int:
        if self.embeddings:
            return len(self.embeddings[0])
        return 0


@dataclass
class SimilarityResult:
    """
    Result of a cosine similarity computation.

    Attributes:
        score: Cosine similarity score between -1 and 1
        text_a: First input text
        text_b: Second input text
    """
    score: float
    text_a: str
    text_b: str


@dataclass
class SearchResult:
    """
    Result of a semantic search operation.

    Attributes:
        document: The matched document text
        score: Similarity score with the query
        index: Original index in the document list
    """
    document: str
    score: float
    index: int


def normalize_embedding(embedding: List[float]) -> List[float]:
    """
    L2-normalize an embedding vector.

    Args:
        embedding: Raw embedding vector from OpenAI API

    Returns:
        L2-normalized embedding vector
    """
    magnitude = math.sqrt(sum(x * x for x in embedding))
    if magnitude == 0:
        return embedding
    return [x / magnitude for x in embedding]


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """
    Compute cosine similarity between two embedding vectors.

    Args:
        vec_a: First embedding vector
        vec_b: Second embedding vector

    Returns:
        Cosine similarity score in range [-1, 1]
    """
    if len(vec_a) != len(vec_b):
        raise ValueError("Embedding vectors must have the same dimension")

    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(x * x for x in vec_a))
    norm_b = math.sqrt(sum(x * x for x in vec_b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


def build_similarity_request(text_a: str, text_b: str) -> EmbeddingRequest:
    """
    Build an EmbeddingRequest for computing similarity between two texts.

    Args:
        text_a: First text
        text_b: Second text

    Returns:
        EmbeddingRequest for both texts
    """
    return EmbeddingRequest(
        texts=[text_a, text_b],
        model=DEFAULT_EMBEDDING_MODEL,
        dimensions=DEFAULT_EMBEDDING_DIMENSIONS,
    )


def format_search_results(
    query: str,
    documents: List[str],
    query_embedding: List[float],
    document_embeddings: List[List[float]],
    top_k: int = 5,
) -> List[SearchResult]:
    """
    Format and rank search results by similarity score.

    Args:
        query: The search query text
        documents: List of document texts
        query_embedding: Embedding of the query
        document_embeddings: Embeddings of all documents
        top_k: Number of top results to return

    Returns:
        List of SearchResult objects ranked by similarity
    """
    results = []
    for idx, (doc, doc_emb) in enumerate(zip(documents, document_embeddings)):
        score = cosine_similarity(query_embedding, doc_emb)
        results.append(SearchResult(document=doc, score=score, index=idx))

    results.sort(key=lambda r: r.score, reverse=True)
    return results[:top_k]
