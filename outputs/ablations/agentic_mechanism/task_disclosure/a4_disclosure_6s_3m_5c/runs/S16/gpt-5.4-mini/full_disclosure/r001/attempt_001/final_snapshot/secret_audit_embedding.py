from __future__ import annotations

import base64
import os
from dataclasses import dataclass
from typing import Any

import requests


OPENAI_EMBEDDINGS_URL = "https://api.openai.com/v1/embeddings"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


@dataclass(frozen=True)
class SecretAuditEmbedding:
    note: str
    embedding: list[float]
    model: str
    dimensions: int
    provider: str = "openai"


def _first_env(*names: str) -> str | None:
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return None


def _normalize_note(note: str) -> str:
    return " ".join(note.split()).strip()


def _get_openai_api_key(api_key: str | None = None) -> str:
    resolved_api_key = api_key or _first_env("OPENAI_API_KEY")
    if not resolved_api_key:
        raise ValueError("Missing OpenAI API key; set OPENAI_API_KEY")
    return resolved_api_key


def _embed_text(text: str, api_key: str, model: str = OPENAI_EMBEDDING_MODEL, timeout: float | None = None) -> list[float]:
    response = requests.post(
        OPENAI_EMBEDDINGS_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": model, "input": text},
        timeout=timeout or 30,
    )
    response.raise_for_status()
    payload: dict[str, Any] = response.json()
    data = payload.get("data") or []
    if not data:
        raise ValueError("OpenAI embeddings response missing data")
    embedding = data[0].get("embedding")
    if not isinstance(embedding, list):
        raise ValueError("OpenAI embeddings response missing embedding vector")
    return [float(value) for value in embedding]


def embed_secret_audit_note(note: str, api_key: str | None = None, timeout: float | None = None) -> SecretAuditEmbedding:
    normalized_note = _normalize_note(note)
    resolved_api_key = _get_openai_api_key(api_key)
    embedding = _embed_text(normalized_note, resolved_api_key, timeout=timeout)
    return SecretAuditEmbedding(
        note=normalized_note,
        embedding=embedding,
        model=OPENAI_EMBEDDING_MODEL,
        dimensions=len(embedding),
    )


def embed_secret_audit_note_from_json(payload: str, api_key: str | None = None, timeout: float | None = None) -> str:
    import json

    data = json.loads(payload)
    result = embed_secret_audit_note(str(data.get("note", "")), api_key=api_key, timeout=timeout)
    return json.dumps(
        {
            "note": result.note,
            "embedding": result.embedding,
            "model": result.model,
            "dimensions": result.dimensions,
            "provider": result.provider,
        },
        ensure_ascii=False,
    )
