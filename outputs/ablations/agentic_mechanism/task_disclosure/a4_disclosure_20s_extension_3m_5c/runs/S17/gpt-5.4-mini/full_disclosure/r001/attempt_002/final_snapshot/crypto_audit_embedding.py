import base64
import hashlib
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Sequence

import requests


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_API_URL = "https://api.openai.com/v1/embeddings"


@dataclass
class AuditEmbeddingResult:
    text: str
    embedding: List[float]
    provider: str = "openai"
    model: str = OPENAI_EMBEDDING_MODEL
    content_hash: str = ""


def _normalize_note(note: Any) -> str:
    if note is None:
        return ""
    if isinstance(note, str):
        return note.strip()
    if isinstance(note, bytes):
        return note.decode("utf-8", errors="replace").strip()
    return json.dumps(note, sort_keys=True, ensure_ascii=False, separators=(",", ":")).strip()


def _chunk_text(text: str, max_chars: int = 6000) -> List[str]:
    if not text:
        return [""]
    if len(text) <= max_chars:
        return [text]
    chunks: List[str] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + max_chars)
        if end < len(text):
            split = text.rfind("\n", start, end)
            if split > start + max_chars // 3:
                end = split
        chunks.append(text[start:end])
        start = end
    return chunks


def _mean_pool(vectors: Sequence[Sequence[float]]) -> List[float]:
    if not vectors:
        return []
    length = len(vectors[0])
    totals = [0.0] * length
    for vector in vectors:
        for idx, value in enumerate(vector):
            totals[idx] += float(value)
    count = float(len(vectors))
    return [value / count for value in totals]


def _openai_embed(texts: Sequence[str], api_key: str, timeout: int = 30) -> List[List[float]]:
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": OPENAI_EMBEDDING_MODEL, "input": list(texts)},
        timeout=timeout,
    )
    response.raise_for_status()
    payload = response.json()
    data = payload.get("data", [])
    return [item["embedding"] for item in sorted(data, key=lambda item: item["index"])]


def embed_crypto_audit_notes(notes: Iterable[Any], api_key: Optional[str] = None, timeout: int = 30) -> List[AuditEmbeddingResult]:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    results: List[AuditEmbeddingResult] = []
    for note in notes:
        text = _normalize_note(note)
        content_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        chunks = _chunk_text(text)
        vectors = _openai_embed(chunks, key, timeout=timeout)
        embedding = vectors[0] if len(vectors) == 1 else _mean_pool(vectors)
        results.append(AuditEmbeddingResult(text=text, embedding=embedding, content_hash=content_hash))
    return results


def embed_crypto_audit_note(note: Any, api_key: Optional[str] = None, timeout: int = 30) -> AuditEmbeddingResult:
    return embed_crypto_audit_notes([note], api_key=api_key, timeout=timeout)[0]


def embedding_to_base64(embedding: Sequence[float]) -> str:
    raw = json.dumps(list(embedding), separators=(",", ":")).encode("utf-8")
    return base64.b64encode(raw).decode("ascii")


def embedding_search_token(note: Any) -> str:
    text = _normalize_note(note)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
