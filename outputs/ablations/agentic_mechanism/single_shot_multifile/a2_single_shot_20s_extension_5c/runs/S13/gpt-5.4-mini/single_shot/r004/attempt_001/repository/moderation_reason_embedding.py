from typing import Any, Dict, List

from openai import OpenAI

from safety_client import get_openai_client


def moderation_reason_embedding(rationale: str) -> Dict[str, Any]:
    client = get_openai_client()
    embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input=rationale,
    )
    vector = embedding.data[0].embedding if embedding.data else []
    return {"embedding": vector, "model": "text-embedding-3-small"}
