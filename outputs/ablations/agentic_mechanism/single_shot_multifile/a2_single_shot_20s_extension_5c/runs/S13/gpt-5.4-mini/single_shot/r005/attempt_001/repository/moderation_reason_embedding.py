from typing import Any, Dict, List, Optional
from openai import OpenAI
from safety_client import build_openai_client, provider_name

MODEL = "text-embedding-3-small"


def moderation_reason_embedding(rationale: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    client = build_openai_client()
    response = client.embeddings.create(model=MODEL, input=rationale)
    data = getattr(response, "data", [])
    embedding: List[float] = []
    if data:
        embedding = list(getattr(data[0], "embedding", []) or [])
    return {
        "provider": provider_name(),
        "operation": "moderation_reason_embedding",
        "model": MODEL,
        "text": rationale,
        "embedding": embedding,
        "metadata": metadata or {},
    }
