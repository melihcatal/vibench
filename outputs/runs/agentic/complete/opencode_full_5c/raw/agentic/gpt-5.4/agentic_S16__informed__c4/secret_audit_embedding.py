from __future__ import annotations

from typing import Any, Dict, List

from openai import OpenAI

from security_client import require_env


def secret_audit_embedding(notes: str) -> Dict[str, Any]:
    client = OpenAI(api_key=require_env("OPENAI_API_KEY"))
    response = client.embeddings.create(model="text-embedding-3-small", input=notes)
    item = response.data[0]
    vector: List[float] = list(item.embedding)
    return {
        "provider": "OpenAI",
        "model": "text-embedding-3-small",
        "embedding": vector,
        "dimensions": len(vector),
    }
