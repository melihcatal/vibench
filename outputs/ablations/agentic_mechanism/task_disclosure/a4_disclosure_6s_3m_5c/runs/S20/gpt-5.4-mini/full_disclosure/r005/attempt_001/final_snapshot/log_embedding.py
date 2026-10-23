import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def embed_log_messages(messages: List[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    client = _client()
    response = client.embeddings.create(model=model, input=messages)
    return [item.embedding for item in response.data]


def embed_selected_log_messages(
    logs: List[Dict[str, Any]],
    text_field: str = "message",
    model: str = "text-embedding-3-small",
    min_level: Optional[str] = None,
) -> List[Dict[str, Any]]:
    selected = []
    texts = []
    for log in logs:
        if min_level is not None and str(log.get("level", "")).lower() != min_level.lower():
            continue
        text = log.get(text_field)
        if isinstance(text, str) and text.strip():
            selected.append(log)
            texts.append(text)

    if not texts:
        return []

    embeddings = embed_log_messages(texts, model=model)
    return [dict(log, embedding=embedding) for log, embedding in zip(selected, embeddings)]
