"""
ocr_embedding.py - Embeds extracted document sections for semantic retrieval
using OpenAI's text embedding models.

Provider: OpenAI
SDK: openai
Model: text-embedding-3-small
Endpoint: api.openai.com
"""

import os
from typing import List, Optional

from document_models import (
    EmbeddingRequest,
    EmbeddingResponse,
    ExtractTextResponse,
)

PROVIDER = "openai"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")


def create_embedding(request: EmbeddingRequest) -> EmbeddingResponse:
    """
    Create an embedding vector for a document section using OpenAI's
    text-embedding-3-small model.

    Args:
        request: EmbeddingRequest with text and optional model name.

    Returns:
        EmbeddingResponse containing the embedding vector.
    """
    from openai import OpenAI

    if not request.text:
        raise ValueError("Text is required for embedding.")

    if not OPENAI_API_KEY:
        raise EnvironmentError("OPENAI_API_KEY environment variable is required.")

    client = OpenAI(api_key=OPENAI_API_KEY)

    model = request.model or OPENAI_EMBEDDING_MODEL

    response = client.embeddings.create(
        model=model,
        input=request.text,
    )

    embedding_data = response.data[0]
    vector = embedding_data.embedding

    token_count = response.usage.total_tokens if response.usage else 0

    return EmbeddingResponse(
        embedding=vector,
        model=response.model,
        token_count=token_count,
        provider=PROVIDER,
        raw_response={
            "id": response.id,
            "created": response.created,
            "usage": token_count,
        },
    )


def embed_ocr_sections(
    ocr_response: ExtractTextResponse,
    section_size: int = 500,
    overlap: int = 50,
    model: Optional[str] = None,
) -> List[EmbeddingResponse]:
    """
    Split OCR-extracted text into overlapping sections and embed each section.

    Args:
        ocr_response: ExtractTextResponse from OCR extraction.
        section_size: Maximum number of characters per section.
        overlap: Number of overlapping characters between sections.
        model: Optional embedding model override.

    Returns:
        List of EmbeddingResponse objects, one per section.
    """
    text = ocr_response.full_text
    if not text:
        return []

    sections = _split_text_with_overlap(text, section_size, overlap)

    embeddings = []
    for section in sections:
        req = EmbeddingRequest(
            text=section,
            model=model or OPENAI_EMBEDDING_MODEL,
        )
        embedding = create_embedding(req)
        embeddings.append(embedding)

    return embeddings


def embed_blocks(
    ocr_response: ExtractTextResponse,
    model: Optional[str] = None,
) -> List[EmbeddingResponse]:
    """
    Embed individual OCR blocks from the extraction response.

    Args:
        ocr_response: ExtractTextResponse from OCR extraction.
        model: Optional embedding model override.

    Returns:
        List of EmbeddingResponse objects, one per block.
    """
    embeddings = []
    target_model = model or OPENAI_EMBEDDING_MODEL

    for block in ocr_response.blocks:
        if block.text.strip():
            req = EmbeddingRequest(
                text=block.text,
                model=target_model,
            )
            embedding = create_embedding(req)
            embeddings.append(embedding)

    if not embeddings and ocr_response.full_text.strip():
        req = EmbeddingRequest(
            text=ocr_response.full_text,
            model=target_model,
        )
        embeddings.append(create_embedding(req))

    return embeddings


def embed_single_text(
    text: str,
    model: Optional[str] = None,
) -> EmbeddingResponse:
    """
    Convenience function to embed a single text string.

    Args:
        text: The text to embed.
        model: Optional embedding model override.

    Returns:
        EmbeddingResponse with the embedding vector.
    """
    req = EmbeddingRequest(
        text=text,
        model=model or OPENAI_EMBEDDING_MODEL,
    )
    return create_embedding(req)


def _split_text_with_overlap(text: str, size: int, overlap: int) -> List[str]:
    """Split text into chunks of given size with overlap."""
    if len(text) <= size:
        return [text]

    sections = []
    start = 0
    while start < len(text):
        end = start + size
        chunk = text[start:end]
        if chunk.strip():
            sections.append(chunk)
        start = end - overlap

    return sections


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """
    Compute cosine similarity between two embedding vectors.

    Args:
        vec_a: First embedding vector.
        vec_b: Second embedding vector.

    Returns:
        Cosine similarity score between 0 and 1.
    """
    import math

    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must have the same dimensionality.")

    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)
