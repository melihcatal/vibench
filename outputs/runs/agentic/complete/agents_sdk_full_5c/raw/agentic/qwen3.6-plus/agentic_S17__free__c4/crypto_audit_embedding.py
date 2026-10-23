"""
Embed crypto audit notes for semantic search using the OpenAI Embeddings API.
Uses the openai python SDK to generate vector embeddings of encryption
audit notes, enabling semantic search and similarity matching.

Provider: OpenAI Embeddings API - api.openai.com
Model: text-embedding-3-small
"""

import json
import logging
import os
from typing import Optional, List, Dict, Any

import numpy as np
from openai import OpenAI

from security_models import EmbeddingRequest, EmbeddingResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenAI Embedding API model identifiers
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_EMBEDDING_MODEL_LARGE = "text-embedding-3-large"
OPENAI_EMBEDDING_DIMENSIONS_SMALL = 1536
OPENAI_EMBEDDING_DIMENSIONS_LARGE = 3072


def create_openai_client(api_key: Optional[str] = None) -> OpenAI:
    """
    Create an OpenAI client for embeddings API calls.
    Provider: OpenAI - api.openai.com
    """
    key = api_key or os.environ.get("OPENAI_API_KEY", "")
    if not key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=key)


def embed_audit_note(
    text: str,
    model: str = OPENAI_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> EmbeddingResponse:
    """
    Embed a single crypto audit note using OpenAI Embeddings API.

    Provider: OpenAI Embeddings API - api.openai.com
    Model: text-embedding-3-small (default) or text-embedding-3-large

    Args:
        text: The audit note text to embed.
        model: Embedding model to use (default: text-embedding-3-small).
        dimensions: Optional output dimensionality.
        api_key: Optional OpenAI API key override.
        metadata: Optional metadata to attach to the embedding.

    Returns:
        EmbeddingResponse with the embedding vector.
    """
    request = EmbeddingRequest(text=text, model=model, metadata=metadata)
    normalized_text = request.to_normalized_text()

    if not normalized_text:
        raise ValueError("Audit note text cannot be empty")

    client = create_openai_client(api_key)

    params: Dict[str, Any] = {
        "input": normalized_text,
        "model": model,
    }
    if dimensions:
        params["dimensions"] = dimensions

    try:
        logger.info("Embedding audit note with OpenAI model %s", model)
        response = client.embeddings.create(**params)

        embedding_vector = response.data[0].embedding

        result = EmbeddingResponse(
            embedding=embedding_vector,
            model=model,
            text=normalized_text,
            metadata=metadata,
        )

        logger.info("Embedding created: %d dimensions, model=%s",
                     len(embedding_vector), model)
        return result

    except Exception as e:
        logger.error("OpenAI Embeddings API error: %s", e)
        raise


def embed_audit_notes_batch(
    texts: List[str],
    model: str = OPENAI_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
    batch_size: int = 100,
) -> List[EmbeddingResponse]:
    """
    Embed multiple crypto audit notes in batch using OpenAI Embeddings API.

    Provider: OpenAI Embeddings API - api.openai.com
    Model: text-embedding-3-small (default)

    Args:
        texts: List of audit note texts.
        model: Embedding model to use.
        dimensions: Optional output dimensionality.
        api_key: Optional API key override.
        batch_size: Maximum batch size per API call (max 2048 for OpenAI).

    Returns:
        List of EmbeddingResponse objects.
    """
    client = create_openai_client(api_key)
    all_results: List[EmbeddingResponse] = []

    params: Dict[str, Any] = {
        "model": model,
    }
    if dimensions:
        params["dimensions"] = dimensions

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        params["input"] = batch

        try:
            logger.info("Embedding batch %d-%d with OpenAI model %s",
                        i, i + len(batch), model)
            response = client.embeddings.create(**params)

            for idx, data in enumerate(response.data):
                result = EmbeddingResponse(
                    embedding=data.embedding,
                    model=model,
                    text=batch[idx],
                )
                all_results.append(result)

        except Exception as e:
            logger.error("OpenAI batch embedding error at offset %d: %s", i, e)
            # Add empty results for failed batch items
            for txt in batch:
                all_results.append(
                    EmbeddingResponse(embedding=[], model=model, text=txt)
                )

    logger.info("Batch embedding complete: %d embeddings created", len(all_results))
    return all_results


def compute_similarity(
    embedding1: List[float],
    embedding2: List[float],
    metric: str = "cosine",
) -> float:
    """
    Compute similarity between two embedding vectors.

    Args:
        embedding1: First embedding vector.
        embedding2: Second embedding vector.
        metric: Similarity metric (cosine, euclidean, dot).

    Returns:
        Similarity score (higher = more similar).
    """
    if not embedding1 or not embedding2:
        return 0.0

    v1 = np.array(embedding1)
    v2 = np.array(embedding2)

    if metric == "cosine":
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return float(np.dot(v1, v2) / (norm1 * norm2))
    elif metric == "dot":
        return float(np.dot(v1, v2))
    elif metric == "euclidean":
        dist = float(np.linalg.norm(v1 - v2))
        # Convert distance to similarity (1 / (1 + distance))
        return 1.0 / (1.0 + dist)
    else:
        raise ValueError(f"Unsupported similarity metric: {metric}")


def search_similar_notes(
    query_text: str,
    stored_embeddings: List[EmbeddingResponse],
    model: str = OPENAI_EMBEDDING_MODEL,
    top_k: int = 5,
    threshold: float = 0.7,
    api_key: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Search for audit notes similar to a query using embeddings.

    Provider: OpenAI Embeddings API - api.openai.com
    Model: text-embedding-3-small

    Args:
        query_text: The search query text.
        stored_embeddings: List of previously computed EmbeddingResponse objects.
        model: Embedding model.
        top_k: Maximum number of results to return.
        threshold: Minimum similarity threshold.
        api_key: Optional API key.

    Returns:
        List of dicts with note text and similarity score, sorted by score.
    """
    query_embedding = embed_audit_note(query_text, model=model, api_key=api_key)

    similarities = []
    for stored in stored_embeddings:
        if not stored.embedding:
            continue
        score = compute_similarity(query_embedding.embedding, stored.embedding)
        if score >= threshold:
            similarities.append({
                "text": stored.text,
                "similarity": round(score, 4),
                "model": stored.model,
                "metadata": stored.metadata,
            })

    similarities.sort(key=lambda x: x["similarity"], reverse=True)
    return similarities[:top_k]


if __name__ == "__main__":
    sample_note = "AES-256-GCM encryption used for PII data at rest. Key rotation scheduled quarterly."
    result = embed_audit_note(sample_note)
    print(result.to_json())
