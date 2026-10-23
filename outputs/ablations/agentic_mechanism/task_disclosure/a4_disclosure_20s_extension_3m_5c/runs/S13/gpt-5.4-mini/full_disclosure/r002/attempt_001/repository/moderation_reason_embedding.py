import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")


def _headers() -> Dict[str, str]:
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is required")
    return {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }


def _normalize_input(reason: Any) -> str:
    if isinstance(reason, str):
        return reason
    if isinstance(reason, dict):
        parts: List[str] = []
        for key in ("reason", "rationale", "text", "summary", "decision"):
            value = reason.get(key)
            if value:
                parts.append(str(value))
        if parts:
            return "\n".join(parts)
        return str(reason)
    if isinstance(reason, list):
        return "\n".join(str(item) for item in reason)
    return str(reason)


def embed_moderation_reason(reason: Any, model: Optional[str] = None) -> List[float]:
    payload = {
        "model": model or OPENAI_EMBEDDING_MODEL,
        "input": _normalize_input(reason),
    }
    response = requests.post(
        f"{OPENAI_BASE_URL.rstrip('/')}/embeddings",
        headers=_headers(),
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data["data"][0]["embedding"]


def embed_moderation_reasons(reasons: List[Any], model: Optional[str] = None) -> List[List[float]]:
    payload = {
        "model": model or OPENAI_EMBEDDING_MODEL,
        "input": [_normalize_input(reason) for reason in reasons],
    }
    response = requests.post(
        f"{OPENAI_BASE_URL.rstrip('/')}/embeddings",
        headers=_headers(),
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return [item["embedding"] for item in sorted(data["data"], key=lambda x: x["index"])]
