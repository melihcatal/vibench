import hashlib
import os
from typing import Any, Dict, List, Optional

import openai
from openai import OpenAI

from security_models import (
    AuditEmbeddingRequest,
    AuditEmbeddingResponse,
    compute_payload_hash,
)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_EMBEDDING_MODEL = os.environ.get(
    "OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"
)
OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")


def get_openai_client() -> OpenAI:
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_API_BASE,
    )


def embed_audit_notes(
    audit_notes: str,
    key_id: Optional[str] = None,
    operation: Optional[str] = None,
    metadata: Optional[Dict[str, str]] = None,
    model: str = OPENAI_EMBEDDING_MODEL,
) -> AuditEmbeddingResponse:
    client = get_openai_client()

    audit_notes_hash = compute_payload_hash(audit_notes)

    embedding_input = audit_notes
    if metadata:
        meta_str = " | ".join(f"{k}={v}" for k, v in metadata.items())
        embedding_input = f"{audit_notes} [{meta_str}]"

    response = client.embeddings.create(
        model=model,
        input=embedding_input,
        encoding_format="float",
    )

    embedding_vector = response.data[0].embedding

    result = AuditEmbeddingResponse(
        embedding=embedding_vector,
        model=model,
        audit_notes_hash=audit_notes_hash,
        key_id=key_id,
    )
    return result


def embed_audit_notes_batch(
    audit_notes_list: List[AuditEmbeddingRequest],
    model: str = OPENAI_EMBEDDING_MODEL,
) -> List[AuditEmbeddingResponse]:
    client = get_openai_client()

    inputs = []
    for req in audit_notes_list:
        embedding_input = req.audit_notes
        if req.metadata:
            meta_str = " | ".join(f"{k}={v}" for k, v in req.metadata.items())
            embedding_input = f"{req.audit_notes} [{meta_str}]"
        inputs.append(embedding_input)

    response = client.embeddings.create(
        model=model,
        input=inputs,
        encoding_format="float",
    )

    results = []
    for i, req in enumerate(audit_notes_list):
        embedding_vector = response.data[i].embedding
        audit_notes_hash = compute_payload_hash(req.audit_notes)

        result = AuditEmbeddingResponse(
            embedding=embedding_vector,
            model=model,
            audit_notes_hash=audit_notes_hash,
            key_id=req.key_id,
        )
        results.append(result)

    return results


def compute_embedding_similarity(
    embedding_a: List[float],
    embedding_b: List[float],
) -> float:
    if len(embedding_a) != len(embedding_b):
        raise ValueError("Embeddings must have the same dimension")

    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    magnitude_a = sum(a * a for a in embedding_a) ** 0.5
    magnitude_b = sum(b * b for b in embedding_b) ** 0.5

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def search_similar_audit_notes(
    query_notes: str,
    stored_embeddings: List[Dict[str, Any]],
    top_k: int = 5,
    model: str = OPENAI_EMBEDDING_MODEL,
) -> List[Dict[str, Any]]:
    query_response = embed_audit_notes(
        audit_notes=query_notes,
        model=model,
    )

    query_embedding = query_response.embedding

    scored_results = []
    for stored in stored_embeddings:
        similarity = compute_embedding_similarity(query_embedding, stored["embedding"])
        scored_results.append(
            {
                "similarity": similarity,
                "audit_notes_hash": stored.get("audit_notes_hash"),
                "key_id": stored.get("key_id"),
                "metadata": stored.get("metadata"),
                "original_notes": stored.get("original_notes"),
            }
        )

    scored_results.sort(key=lambda x: x["similarity"], reverse=True)
    return scored_results[:top_k]


def create_audit_embedding_index(
    audit_entries: List[Dict[str, str]],
    model: str = OPENAI_EMBEDDING_MODEL,
) -> List[Dict[str, Any]]:
    client = get_openai_client()

    inputs = [entry["audit_notes"] for entry in audit_entries]

    response = client.embeddings.create(
        model=model,
        input=inputs,
        encoding_format="float",
    )

    index = []
    for i, entry in enumerate(audit_entries):
        embedding_vector = response.data[i].embedding
        audit_notes_hash = compute_payload_hash(entry["audit_notes"])

        index.append(
            {
                "embedding": embedding_vector,
                "audit_notes_hash": audit_notes_hash,
                "key_id": entry.get("key_id"),
                "metadata": entry.get("metadata", {}),
                "original_notes": entry["audit_notes"],
                "model": model,
            }
        )

    return index
