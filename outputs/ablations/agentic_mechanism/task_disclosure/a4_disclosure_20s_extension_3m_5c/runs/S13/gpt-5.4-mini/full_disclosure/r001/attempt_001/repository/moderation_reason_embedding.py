from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence

import requests


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_API_URL = "https://api.openai.com/v1/embeddings"


@dataclass(frozen=True)
class ModerationReasonEmbedding:
    text: str
    embedding: Sequence[float]
    metadata: Mapping[str, Any]


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    return value if value not in (None, "") else default


def _normalize_reason(reason: Any) -> str:
    if reason is None:
        return ""
    if isinstance(reason, str):
        return reason.strip()
    return str(reason).strip()


def _extract_text(record: Any) -> str:
    if isinstance(record, str):
        return record.strip()
    if isinstance(record, Mapping):
        for key in ("rationale", "reason", "text", "summary", "message"):
            value = record.get(key)
            if value:
                return _normalize_reason(value)
    return _normalize_reason(record)


def embed_moderation_rationales(
    rationales: Iterable[Any],
    *,
    api_key: Optional[str] = None,
    model: str = OPENAI_EMBEDDING_MODEL,
    timeout: float = 30.0,
) -> List[ModerationReasonEmbedding]:
    key = api_key or _env("OPENAI_API_KEY")
    if not key:
        raise ValueError("Missing OpenAI API key")

    texts = [_extract_text(item) for item in rationales]
    if not texts:
        return []

    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={"model": model, "input": texts},
        timeout=timeout,
    )
    response.raise_for_status()
    payload = response.json()
    data = payload.get("data", [])
    embeddings_by_index: Dict[int, Sequence[float]] = {}
    for item in data:
        if isinstance(item, Mapping) and "index" in item and "embedding" in item:
            embeddings_by_index[int(item["index"])] = item["embedding"]

    results: List[ModerationReasonEmbedding] = []
    for index, text in enumerate(texts):
        results.append(
            ModerationReasonEmbedding(
                text=text,
                embedding=embeddings_by_index.get(index, []),
                metadata={"model": model, "index": index, "provider": "openai"},
            )
        )
    return results
