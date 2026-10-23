from __future__ import annotations

from typing import Any, Dict, List

from openai import OpenAI


def crypto_audit_embedding(notes: List[str]) -> Dict[str, Any]:
    client = OpenAI()
    response = client.embeddings.create(model="text-embedding-3-small", input=notes)
    return {"model": "text-embedding-3-small", "embeddings": [item.embedding for item in response.data]}
