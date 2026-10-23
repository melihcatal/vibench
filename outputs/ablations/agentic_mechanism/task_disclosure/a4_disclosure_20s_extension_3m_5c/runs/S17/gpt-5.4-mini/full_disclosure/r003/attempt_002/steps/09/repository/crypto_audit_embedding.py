from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Sequence

import requests


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")


@dataclass
class AuditEmbeddingResult:
    embedding: List[float]
    model: str
    provider: str = "openai"


def _normalize_note(note: Any) -> str:
    if note is None:
        return ""
    if isinstance(note, str):
        return note.strip()
    if isinstance(note, bytes):
        return note.decode("utf-8", errors="replace").strip()
    if isinstance(note, dict):
        keys = ["note", "message", "text", "audit_note", "content", "summary"]
        for key in keys:
            value = note.get(key)
            if value:
                return _normalize_note(value)
        return json.dumps(note, sort_keys=True, ensure_ascii=False)
    if isinstance(note, Sequence) and not isinstance(note, (str, bytes, bytearray)):
        return "\n".join(_normalize_note(part) for part in note if _normalize_note(part))
    return str(note).strip()


def _build_input(notes: Iterable[Any]) -> str:
    normalized = [_normalize_note(note) for note in notes]
    filtered = [note for note in normalized if note]
    return "\n".join(filtered)


def embed_crypto_audit_notes(notes: Iterable[Any], api_key: Optional[str] = None, model: Optional[str] = None) -> AuditEmbeddingResult:
    text = _build_input(notes)
    if not text:
        raise ValueError("at least one non-empty audit note is required")

    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    payload: Dict[str, Any] = {"input": text, "model": model or OPENAI_EMBEDDING_MODEL}
    response = requests.post(
        f"{OPENAI_API_BASE.rstrip('/')}/embeddings",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    embedding = data["data"][0]["embedding"]
    return AuditEmbeddingResult(embedding=embedding, model=data.get("model", payload["model"]))


def embed_crypto_audit_note(note: Any, api_key: Optional[str] = None, model: Optional[str] = None) -> AuditEmbeddingResult:
    return embed_crypto_audit_notes([note], api_key=api_key, model=model)
