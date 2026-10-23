"""
asset_metadata_embedding.py - Embed object metadata and extracted text for search.

Uses OpenAI Embeddings API via openai SDK with text-embedding-3-small model
as the concrete hosted embeddings provider.
Authentication via OPENAI_API_KEY environment variable.
"""

import os
import json
from typing import Optional, List, Dict, Any
from openai import OpenAI


def embed_text(
    text: str,
    model: str = "text-embedding-3-small",
    api_key: Optional[str] = None,
    dimensions: Optional[int] = None,
) -> List[float]:
    """
    Generate an embedding vector for a text string using OpenAI Embeddings API.

    Args:
        text: Input text to embed.
        model: OpenAI embedding model identifier (default: text-embedding-3-small).
        api_key: OpenAI API key. Falls back to OPENAI_API_KEY env var.
        dimensions: Optional output dimensionality (e.g., 256, 512, 1024, 1536).

    Returns:
        List of floats representing the embedding vector.

    Raises:
        ValueError: If text is empty.
        RuntimeError: If embedding generation fails.
    """
    if not text or not text.strip():
        raise ValueError("Input text is required for embedding.")

    openai_api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError(
            "OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key."
        )

    client = OpenAI(api_key=openai_api_key)

    # Truncate text to fit within model token limits
    max_chars = 8000
    if len(text) > max_chars:
        text = text[:max_chars]

    params = {
        "model": model,
        "input": text,
    }

    if dimensions:
        params["dimensions"] = dimensions

    try:
        response = client.embeddings.create(**params)
        return response.data[0].embedding

    except Exception as e:
        raise RuntimeError(f"OpenAI text-embedding-3-small embedding generation failed: {e}") from e


def embed_text_batch(
    texts: List[str],
    model: str = "text-embedding-3-small",
    api_key: Optional[str] = None,
    dimensions: Optional[int] = None,
) -> List[List[float]]:
    """
    Generate embedding vectors for a batch of texts using OpenAI Embeddings API.

    Args:
        texts: List of input texts to embed.
        model: OpenAI embedding model identifier.
        api_key: OpenAI API key.
        dimensions: Optional output dimensionality.

    Returns:
        List of embedding vectors (one per input text).
    """
    if not texts:
        return []

    openai_api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OpenAI API key is required.")

    client = OpenAI(api_key=openai_api_key)

    # Truncate each text
    max_chars = 8000
    truncated_texts = [
        t[:max_chars] if len(t) > max_chars else t for t in texts
    ]

    params = {
        "model": model,
        "input": truncated_texts,
    }

    if dimensions:
        params["dimensions"] = dimensions

    try:
        response = client.embeddings.create(**params)
        return [item.embedding for item in response.data]

    except Exception as e:
        raise RuntimeError(f"OpenAI batch embedding generation failed: {e}") from e


def embed_asset_metadata(
    object_key: str,
    bucket_name: str,
    extracted_text: str,
    user_metadata: Optional[Dict[str, str]] = None,
    content_type: Optional[str] = None,
    model: str = "text-embedding-3-small",
    api_key: Optional[str] = None,
    dimensions: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Create a combined embedding for an asset including its metadata and extracted text.

    Constructs a structured representation combining object metadata with extracted
    content, then generates an embedding suitable for semantic search.

    Args:
        object_key: S3 object key or storage identifier.
        bucket_name: Storage bucket name.
        extracted_text: Text extracted from the asset (e.g., via OCR).
        user_metadata: Optional user-defined metadata key-value pairs.
        content_type: Optional MIME content type of the asset.
        model: OpenAI embedding model identifier.
        api_key: OpenAI API key.
        dimensions: Optional output dimensionality.

    Returns:
        Dictionary containing the asset identifier, combined text, and embedding vector.
    """
    openai_api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OpenAI API key is required.")

    # Build combined text representation for embedding
    metadata_parts = [
        f"Object: {object_key}",
        f"Bucket: {bucket_name}",
    ]

    if content_type:
        metadata_parts.append(f"Content Type: {content_type}")

    if user_metadata:
        for key, value in user_metadata.items():
            metadata_parts.append(f"{key}: {value}")

    if extracted_text:
        metadata_parts.append(f"Content: {extracted_text}")

    combined_text = "\n".join(metadata_parts)

    # Generate embedding
    embedding = embed_text(
        text=combined_text,
        model=model,
        api_key=openai_api_key,
        dimensions=dimensions,
    )

    return {
        "object_key": object_key,
        "bucket_name": bucket_name,
        "content_type": content_type,
        "user_metadata": user_metadata or {},
        "embedding_model": model,
        "embedding_dimensions": len(embedding),
        "embedding": embedding,
    }


def compute_cosine_similarity(
    embedding_a: List[float],
    embedding_b: List[float],
) -> float:
    """
    Compute cosine similarity between two embedding vectors.

    Args:
        embedding_a: First embedding vector.
        embedding_b: Second embedding vector.

    Returns:
        Cosine similarity score between 0 and 1.
    """
    if len(embedding_a) != len(embedding_b):
        raise ValueError("Embedding vectors must have the same dimensionality.")

    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    magnitude_a = sum(a * a for a in embedding_a) ** 0.5
    magnitude_b = sum(b * b for b in embedding_b) ** 0.5

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def search_similar_assets(
    query_text: str,
    asset_embeddings: List[Dict[str, Any]],
    top_k: int = 5,
    model: str = "text-embedding-3-small",
    api_key: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Find the most similar assets to a query text using cosine similarity.

    Args:
        query_text: Search query text.
        asset_embeddings: List of pre-computed asset embedding dicts.
        top_k: Number of top results to return.
        model: OpenAI embedding model for query.
        api_key: OpenAI API key.

    Returns:
        Sorted list of asset dicts with similarity scores.
    """
    query_embedding = embed_text(
        text=query_text,
        model=model,
        api_key=api_key,
    )

    scored_assets = []
    for asset in asset_embeddings:
        similarity = compute_cosine_similarity(
            query_embedding, asset["embedding"]
        )
        scored_assets.append({
            **asset,
            "similarity_score": similarity,
        })

    scored_assets.sort(key=lambda x: x["similarity_score"], reverse=True)
    return scored_assets[:top_k]
