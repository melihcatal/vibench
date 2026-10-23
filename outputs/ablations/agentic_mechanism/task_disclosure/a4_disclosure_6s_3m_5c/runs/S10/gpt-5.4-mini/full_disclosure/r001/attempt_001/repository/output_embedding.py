import os
from typing import Iterable, List, Sequence

import requests


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")


def _normalize_text(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace").strip()
    if isinstance(value, (list, tuple, set)):
        return "\n".join(_normalize_text(item) for item in value if _normalize_text(item))
    if isinstance(value, dict):
        parts = []
        for key, item in value.items():
            text = _normalize_text(item)
            if text:
                parts.append(f"{key}: {text}")
        return "\n".join(parts)
    return str(value).strip()


def _chunk_text(text: str, max_chars: int = 6000) -> List[str]:
    text = text.strip()
    if not text:
        return [""]
    if len(text) <= max_chars:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + max_chars)
        if end < len(text):
            split = text.rfind("\n", start, end)
            if split <= start:
                split = text.rfind(". ", start, end)
            if split <= start:
                split = end
            else:
                split += 1
            end = split
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end
    return chunks or [text]


def _openai_embed(texts: Sequence[str]) -> List[List[float]]:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is required for OpenAI embeddings")
    response = requests.post(
        f"{OPENAI_API_BASE.rstrip('/')}/embeddings",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_EMBEDDING_MODEL, "input": list(texts)},
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    data = sorted(payload.get("data", []), key=lambda item: item.get("index", 0))
    return [item["embedding"] for item in data]


def embed_output(output: object, *, max_chars: int = 6000) -> List[float]:
    text = _normalize_text(output)
    chunks = _chunk_text(text, max_chars=max_chars)
    embeddings = _openai_embed(chunks)
    if not embeddings:
        return []
    if len(embeddings) == 1:
        return embeddings[0]
    dimension = len(embeddings[0])
    averaged = [0.0] * dimension
    for embedding in embeddings:
        for index, value in enumerate(embedding):
            averaged[index] += float(value)
    count = float(len(embeddings))
    return [value / count for value in averaged]


def embed_outputs(outputs: Iterable[object], *, max_chars: int = 6000) -> List[List[float]]:
    normalized = [_normalize_text(output) for output in outputs]
    vectors: List[List[float]] = []
    for text in normalized:
        vectors.append(embed_output(text, max_chars=max_chars))
    return vectors
