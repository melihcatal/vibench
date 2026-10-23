"""
Embed secret audit notes for semantic search using OpenAI Embeddings API.

Generates vector embeddings for audit notes associated with secret rotation
events, enabling semantic similarity search across audit records.

Provider: OpenAI / Azure OpenAI embeddings
SDK: openai
Auth: OPENAI_API_KEY
Model: text-embedding-3-small
"""

import os
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

from openai import OpenAI

# OpenAI provider configuration
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def _get_openai_client() -> OpenAI:
    """Create an OpenAI client using the API key from environment."""
    api_key = os.environ.get(OPENAI_API_KEY_ENV)
    if not api_key:
        raise ValueError(
            f"Set the {OPENAI_API_KEY_ENV} environment variable "
            f"with your OpenAI API key."
        )
    return OpenAI(api_key=api_key)


def embed_audit_note(
    audit_note: str,
    model: str = OPENAI_EMBEDDING_MODEL,
) -> Dict[str, Any]:
    """
    Generate an embedding for a single audit note using OpenAI Embeddings API.

    Args:
        audit_note: The audit note text to embed.
        model: OpenAI embedding model identifier (default: text-embedding-3-small).

    Returns:
        Dictionary with the embedding vector and metadata.
    """
    try:
        client = _get_openai_client()

        response = client.embeddings.create(
            model=model,
            input=audit_note,
            encoding_format="float",
        )

        embedding_data = response.data[0]
        embedding_vector = embedding_data.embedding

        result = {
            "success": True,
            "embedding": embedding_vector,
            "model_used": model,
            "provider": "openai",
            "input_tokens": response.usage.prompt_tokens,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "vector_dimension": len(embedding_vector),
        }
        return result

    except Exception as e:
        return {
            "success": False,
            "error_code": "OPENAI_EMBEDDING_ERROR",
            "error_message": str(e),
            "provider": "openai",
            "model_used": model,
        }


def embed_audit_notes_batch(
    audit_notes: List[Dict[str, Any]],
    model: str = OPENAI_EMBEDDING_MODEL,
    batch_size: int = 100,
) -> Dict[str, Any]:
    """
    Generate embeddings for a batch of audit notes using OpenAI Embeddings API.

    Each note dict should have 'note_id' and 'text' keys. The OpenAI API
    supports up to 2048 inputs per request for embedding models.

    Args:
        audit_notes: List of dicts with 'note_id' and 'text' keys.
        model: OpenAI embedding model identifier.
        batch_size: Maximum number of notes per API request.

    Returns:
        Dictionary with batch embedding results and metadata.
    """
    try:
        client = _get_openai_client()

        all_embeddings: List[Dict[str, Any]] = []
        total_tokens = 0
        errors: List[Dict[str, Any]] = []

        for i in range(0, len(audit_notes), batch_size):
            batch = audit_notes[i : i + batch_size]
            texts = [note.get("text", "") for note in batch]

            response = client.embeddings.create(
                model=model,
                input=texts,
                encoding_format="float",
            )

            total_tokens += response.usage.prompt_tokens

            for idx, emb_data in enumerate(response.data):
                original_note = batch[idx]
                all_embeddings.append({
                    "note_id": original_note.get("note_id", f"idx_{i + idx}"),
                    "embedding": emb_data.embedding,
                    "secret_id": original_note.get("secret_id", ""),
                    "timestamp": original_note.get("timestamp", ""),
                })

        result = {
            "success": True,
            "embeddings": all_embeddings,
            "total_embedded": len(all_embeddings),
            "total_tokens": total_tokens,
            "model_used": model,
            "provider": "openai",
            "vector_dimension": len(all_embeddings[0]["embedding"]) if all_embeddings else 0,
            "errors": errors,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        return result

    except Exception as e:
        return {
            "success": False,
            "error_code": "OPENAI_BATCH_EMBEDDING_ERROR",
            "error_message": str(e),
            "provider": "openai",
            "model_used": model,
        }


def compute_similarity(
    embedding_a: List[float],
    embedding_b: List[float],
) -> float:
    """
    Compute cosine similarity between two embedding vectors.

    Args:
        embedding_a: First embedding vector.
        embedding_b: Second embedding vector.

    Returns:
        Cosine similarity score between 0.0 and 1.0.
    """
    if len(embedding_a) != len(embedding_b):
        raise ValueError("Embedding vectors must have the same dimension.")

    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    magnitude_a = sum(a * a for a in embedding_a) ** 0.5
    magnitude_b = sum(b * b for b in embedding_b) ** 0.5

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def search_similar_audit_notes(
    query_embedding: List[float],
    embedded_notes: List[Dict[str, Any]],
    top_k: int = 5,
) -> List[Dict[str, Any]]:
    """
    Find the most similar audit notes to a query embedding.

    Args:
        query_embedding: Embedding vector for the search query.
        embedded_notes: List of dicts with 'embedding' and metadata keys.
        top_k: Number of top results to return.

    Returns:
        List of results sorted by similarity score.
    """
    scored = []
    for note in embedded_notes:
        score = compute_similarity(query_embedding, note["embedding"])
        scored.append({
            "note_id": note.get("note_id", ""),
            "secret_id": note.get("secret_id", ""),
            "similarity": score,
            "timestamp": note.get("timestamp", ""),
        })

    scored.sort(key=lambda x: x["similarity"], reverse=True)
    return scored[:top_k]
