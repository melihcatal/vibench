"""
crypto_audit_embedding.py - Embed crypto audit notes for semantic search using OpenAI Embeddings API.

Uses OpenAI Embeddings API via openai SDK.
Provider signals: openai SDK import, OPENAI_API_KEY auth,
text-embedding-3-small model identifier, api.openai.com endpoint.
"""

import os
import json
from typing import Dict, List, Optional, Any

from openai import OpenAI


def get_openai_client(api_key: Optional[str] = None) -> OpenAI:
    """Create an OpenAI client using OPENAI_API_KEY environment variable."""
    key = api_key or os.environ.get("OPENAI_API_KEY", "")
    if not key:
        raise ValueError("OPENAI_API_KEY environment variable is required.")
    return OpenAI(api_key=key)


def embed_audit_notes(
    notes: List[str],
    model: str = "text-embedding-3-small",
) -> List[Dict[str, Any]]:
    """
    Embed crypto audit notes using OpenAI text-embedding-3-small model.

    OpenAI provider: Uses the Embeddings API at api.openai.com
    with the text-embedding-3-small model via the openai Python SDK.
    Returns embeddings as lists of floats.
    """
    client = get_openai_client()

    response = client.embeddings.create(
        input=notes,
        model="text-embedding-3-small",
    )

    embedded_results = []
    for item in response.data:
        embedded_results.append({
            "index": item.index,
            "embedding": item.embedding,
            "text": notes[item.index] if item.index < len(notes) else "",
        })

    return embedded_results


def embed_single_note(
    note: str,
    model: str = "text-embedding-3-small",
) -> Dict[str, Any]:
    """Embed a single audit note and return the result."""
    results = embed_audit_notes([note], model=model)
    if results:
        return results[0]
    return {"error": "No embedding returned"}


def search_audit_notes_semantic(
    query: str,
    notes: List[str],
    embeddings: Optional[List[List[float]]] = None,
    top_k: int = 3,
    model: str = "text-embedding-3-small",
) -> List[Dict[str, Any]]:
    """
    Perform semantic search over crypto audit notes using OpenAI embeddings.

    Embeds the query with text-embedding-3-small model, then computes
    cosine similarity against pre-computed or on-the-fly embeddings.
    """
    client = get_openai_client()

    query_embedding_response = client.embeddings.create(
        input=query,
        model="text-embedding-3-small",
    )
    query_vector = query_embedding_response.data[0].embedding

    if embeddings is None:
        note_embeddings = embed_audit_notes(notes, model=model)
        vectors = [item["embedding"] for item in note_embeddings]
    else:
        vectors = embeddings

    scored_notes = []
    for i, vector in enumerate(vectors):
        similarity = cosine_similarity(query_vector, vector)
        scored_notes.append({
            "index": i,
            "note": notes[i] if i < len(notes) else "",
            "similarity": similarity,
        })

    scored_notes.sort(key=lambda x: x["similarity"], reverse=True)
    return scored_notes[:top_k]


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Compute cosine similarity between two vectors."""
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = sum(a * a for a in vec_a) ** 0.5
    norm_b = sum(b * b for b in vec_b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def store_embeddings_index(
    notes: List[str],
    output_file: str,
    model: str = "text-embedding-3-small",
) -> Dict[str, Any]:
    """
    Embed audit notes and store them in a JSON index file for later semantic search.
    Uses OpenAI text-embedding-3-small model via api.openai.com.
    """
    embedded_results = embed_audit_notes(notes, model=model)

    index_data = {
        "model": model,
        "provider": "OpenAI Embeddings API (api.openai.com)",
        "note_count": len(notes),
        "notes": notes,
        "embeddings": embedded_results,
    }

    with open(output_file, "w") as f:
        json.dump(index_data, f, indent=2)

    return {
        "status": "success",
        "file": output_file,
        "note_count": len(notes),
        "model": model,
    }


if __name__ == "__main__":
    sample_notes = [
        "KMS key rotation completed on 2024-01-15 for production environment.",
        "Encryption audit: all AES-256-GCM keys are compliant with company policy.",
        "Alert: ECDSA signing key mrk-def456 showed elevated failure rate.",
        "Compliance review: envelope encryption verified for all PII data stores.",
    ]

    try:
        results = embed_audit_notes(sample_notes)
        print(f"Embedded {len(results)} audit notes.")
        print(f"Embedding dimensions: {len(results[0]['embedding'])}")
        print(f"Provider: OpenAI Embeddings API (text-embedding-3-small)")
    except ValueError as e:
        print(f"Error: {e}")
        print("Set OPENAI_API_KEY environment variable to generate embeddings.")
