import os
import json
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone

import openai
from openai import OpenAI

from security_models import AuditNoteEmbedding

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small")


def embed_audit_note(
    note_text: str,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    key_id: Optional[str] = None,
) -> Dict[str, Any]:
    target_model = model or EMBEDDING_MODEL
    target_api_key = api_key or OPENAI_API_KEY
    target_base_url = base_url or OPENAI_BASE_URL

    if not target_api_key:
        raise ValueError(
            "OpenAI API key is required. Set OPENAI_API_KEY environment variable."
        )

    client = OpenAI(api_key=target_api_key, base_url=target_base_url)

    response = client.embeddings.create(
        model=target_model,
        input=note_text,
        encoding_format="float",
    )

    embedding_data = response.data[0].embedding

    audit_embedding = AuditNoteEmbedding(
        note_text=note_text[:1000],
        embedding=embedding_data,
        model=target_model,
        timestamp=datetime.now(timezone.utc).isoformat(),
        key_id=key_id,
    )

    return {
        "embedding": audit_embedding.embedding,
        "model": audit_embedding.model,
        "timestamp": audit_embedding.timestamp,
        "note_preview": audit_embedding.note_text,
        "key_id": audit_embedding.key_id,
        "embedding_dimension": len(audit_embedding.embedding),
    }


def embed_audit_notes_batch(
    notes: List[str],
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    key_id: Optional[str] = None,
    batch_size: int = 100,
) -> List[Dict[str, Any]]:
    target_model = model or EMBEDDING_MODEL
    target_api_key = api_key or OPENAI_API_KEY
    target_base_url = base_url or OPENAI_BASE_URL

    if not target_api_key:
        raise ValueError(
            "OpenAI API key is required. Set OPENAI_API_KEY environment variable."
        )

    client = OpenAI(api_key=target_api_key, base_url=target_base_url)
    all_results = []

    for i in range(0, len(notes), batch_size):
        batch = notes[i : i + batch_size]
        response = client.embeddings.create(
            model=target_model,
            input=batch,
            encoding_format="float",
        )

        for item in response.data:
            audit_embedding = AuditNoteEmbedding(
                note_text=batch[item.index][:1000],
                embedding=item.embedding,
                model=target_model,
                timestamp=datetime.now(timezone.utc).isoformat(),
                key_id=key_id,
            )
            all_results.append(
                {
                    "index": item.index,
                    "embedding": audit_embedding.embedding,
                    "model": audit_embedding.model,
                    "timestamp": audit_embedding.timestamp,
                    "note_preview": audit_embedding.note_text,
                    "key_id": audit_embedding.key_id,
                    "embedding_dimension": len(audit_embedding.embedding),
                }
            )

    return all_results


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
    query_note: str,
    candidate_notes: List[str],
    candidate_embeddings: List[List[float]],
    top_k: int = 5,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> List[Dict[str, Any]]:
    query_result = embed_audit_note(
        note_text=query_note,
        model=model,
        api_key=api_key,
        base_url=base_url,
    )
    query_embedding = query_result["embedding"]

    similarities = []
    for idx, candidate_embedding in enumerate(candidate_embeddings):
        sim = compute_embedding_similarity(query_embedding, candidate_embedding)
        similarities.append((idx, sim, candidate_notes[idx]))

    similarities.sort(key=lambda x: x[1], reverse=True)

    return [
        {
            "rank": rank + 1,
            "index": idx,
            "similarity_score": round(score, 6),
            "note_text": text[:500],
        }
        for rank, (idx, score, text) in enumerate(similarities[:top_k])
    ]
