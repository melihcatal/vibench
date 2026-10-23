from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from pydantic import BaseModel, Field


class EmbeddingRequest(BaseModel):
    """Request model for embedding generation."""

    text: str = Field(..., description="Text to embed")
    model: str = Field(
        default="text-embedding-3-small",
        description="OpenAI embedding model identifier",
    )
    normalize: bool = Field(
        default=False, description="Whether to normalize the embedding vector"
    )


class BatchEmbeddingRequest(BaseModel):
    """Request model for batch embedding generation."""

    texts: List[str] = Field(..., description="List of texts to embed")
    model: str = Field(
        default="text-embedding-3-small",
        description="OpenAI embedding model identifier",
    )
    normalize: bool = Field(
        default=False, description="Whether to normalize the embedding vectors"
    )


class EmbeddingResponse(BaseModel):
    """Response model for embedding generation."""

    embedding: List[float] = Field(..., description="Generated embedding vector")
    model: str = Field(..., description="Model used for embedding")
    text_length: int = Field(..., description="Length of input text")
    normalized: bool = Field(
        default=False, description="Whether embedding is normalized"
    )


class BatchEmbeddingResponse(BaseModel):
    """Response model for batch embedding generation."""

    embeddings: List[List[float]] = Field(
        ..., description="List of generated embedding vectors"
    )
    model: str = Field(..., description="Model used for embedding")
    texts_count: int = Field(..., description="Number of texts processed")
    normalized: bool = Field(
        default=False, description="Whether embeddings are normalized"
    )


class SimilarityRequest(BaseModel):
    """Request model for similarity computation."""

    text1: str = Field(..., description="First text")
    text2: str = Field(..., description="Second text")
    model: str = Field(
        default="text-embedding-3-small",
        description="OpenAI embedding model identifier",
    )


class SimilarityResponse(BaseModel):
    """Response model for similarity computation."""

    similarity: float = Field(..., description="Cosine similarity score")
    model: str = Field(..., description="Model used for embedding")
    texts: List[str] = Field(..., description="Input texts")


class SearchEmbeddingRequest(BaseModel):
    """Request model for search embedding."""

    query: str = Field(..., description="Search query")
    documents: List[str] = Field(
        default_factory=list, description="Documents to search against"
    )
    model: str = Field(
        default="text-embedding-3-small",
        description="OpenAI embedding model identifier",
    )


class SearchEmbeddingResponse(BaseModel):
    """Response model for search embedding."""

    query_embedding: List[float] = Field(..., description="Query embedding vector")
    document_embeddings: List[List[float]] = Field(
        ..., description="Document embedding vectors"
    )
    model: str = Field(..., description="Model used for embedding")
    documents_count: int = Field(..., description="Number of documents")


@dataclass
class EmbeddingJobResult:
    """Data class for embedding job results."""

    text: str
    embedding: List[float]
    processing_time: float
    success: bool
    error: Optional[str] = None


def create_embedding_response(
    embedding: List[float], model: str, text: str, normalized: bool = False
) -> EmbeddingResponse:
    """Create an EmbeddingResponse from embedding data."""
    return EmbeddingResponse(
        embedding=embedding, model=model, text_length=len(text), normalized=normalized
    )


def create_batch_embedding_response(
    embeddings: List[List[float]],
    model: str,
    texts: List[str],
    normalized: bool = False,
) -> BatchEmbeddingResponse:
    """Create a BatchEmbeddingResponse from batch embedding data."""
    return BatchEmbeddingResponse(
        embeddings=embeddings,
        model=model,
        texts_count=len(texts),
        normalized=normalized,
    )
