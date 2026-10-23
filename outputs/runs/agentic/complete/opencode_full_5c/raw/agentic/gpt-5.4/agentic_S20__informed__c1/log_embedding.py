from __future__ import annotations

from typing import Any, Dict, Iterable, List

from openai import OpenAI


def embed_log_messages(
    messages: Iterable[str], model: str = "text-embedding-3-small"
) -> List[Dict[str, Any]]:
    client = OpenAI()
    response = client.embeddings.create(model=model, input=list(messages))
    return [
        {
            "index": item.index,
            "embedding": item.embedding,
            "model": response.model,
        }
        for item in response.data
    ]
