import os
from typing import Any, Dict, Iterable, List, Optional

import requests


OPENAI_EMBEDDINGS_URL = "https://api.openai.com/v1/embeddings"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def _prepare_inputs(messages: Iterable[Any]) -> List[str]:
    texts = [_normalize_text(message) for message in messages]
    return [text for text in texts if text]


def embed_log_messages(
    messages: Iterable[Any],
    api_key: Optional[str] = None,
    model: str = OPENAI_EMBEDDING_MODEL,
    timeout: int = 30,
) -> List[Dict[str, Any]]:
    inputs = _prepare_inputs(messages)
    if not inputs:
        return []

    token = api_key or os.environ.get("OPENAI_API_KEY")
    if not token:
        raise ValueError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_EMBEDDINGS_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={"model": model, "input": inputs},
        timeout=timeout,
    )
    response.raise_for_status()
    payload = response.json()

    results = []
    for item in payload.get("data", []):
        results.append(
            {
                "index": item.get("index"),
                "embedding": item.get("embedding", []),
                "object": item.get("object"),
                "model": payload.get("model", model),
            }
        )
    return results


def embed_log_messages_by_text(
    messages: Iterable[str],
    api_key: Optional[str] = None,
    model: str = OPENAI_EMBEDDING_MODEL,
    timeout: int = 30,
) -> Dict[str, Any]:
    embeddings = embed_log_messages(messages, api_key=api_key, model=model, timeout=timeout)
    return {"model": model, "embeddings": embeddings}
