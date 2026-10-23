import os
import json
from typing import Any, Dict, List, Optional

import requests


OPENAI_EMBEDDINGS_URL = "https://api.openai.com/v1/embeddings"
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def _api_key() -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return key


def _normalize_notes(notes: Any) -> str:
    if notes is None:
        return ""
    if isinstance(notes, str):
        return notes.strip()
    if isinstance(notes, dict):
        return json.dumps(notes, sort_keys=True, separators=(",", ":"))
    if isinstance(notes, list):
        return "\n".join(_normalize_notes(item) for item in notes if item is not None)
    return str(notes).strip()


def embed_crypto_audit_notes(notes: Any, *, model: Optional[str] = None, timeout: int = 30) -> Dict[str, Any]:
    text = _normalize_notes(notes)
    if not text:
        raise ValueError("notes must not be empty")

    payload = {"input": text, "model": model or OPENAI_EMBEDDING_MODEL}
    headers = {
        "Authorization": f"Bearer {_api_key()}",
        "Content-Type": "application/json",
    }
    response = requests.post(OPENAI_EMBEDDINGS_URL, headers=headers, json=payload, timeout=timeout)
    response.raise_for_status()
    data = response.json()
    embedding = data["data"][0]["embedding"]
    return {"text": text, "model": payload["model"], "embedding": embedding, "raw": data}


def embed_many_crypto_audit_notes(notes_list: List[Any], *, model: Optional[str] = None, timeout: int = 30) -> List[Dict[str, Any]]:
    if not notes_list:
        return []
    texts = [_normalize_notes(item) for item in notes_list]
    texts = [text for text in texts if text]
    if not texts:
        raise ValueError("notes_list must contain at least one non-empty item")

    payload = {"input": texts, "model": model or OPENAI_EMBEDDING_MODEL}
    headers = {
        "Authorization": f"Bearer {_api_key()}",
        "Content-Type": "application/json",
    }
    response = requests.post(OPENAI_EMBEDDINGS_URL, headers=headers, json=payload, timeout=timeout)
    response.raise_for_status()
    data = response.json()
    results = []
    for item in data["data"]:
        results.append({"index": item["index"], "embedding": item["embedding"]})
    return results
