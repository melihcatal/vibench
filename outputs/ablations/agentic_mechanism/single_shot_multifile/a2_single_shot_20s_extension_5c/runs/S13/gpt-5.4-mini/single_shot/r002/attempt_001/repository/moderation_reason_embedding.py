from typing import Dict, List
from openai import OpenAI
from safety_client import get_openai_client

EMBEDDING_MODEL = "text-embedding-3-small"


def moderation_reason_embedding(rationale: str, client: OpenAI = None) -> Dict[str, List[float]]:
    client = client or get_openai_client()
    resp = client.embeddings.create(model=EMBEDDING_MODEL, input=rationale)
    return {"embedding": resp.data[0].embedding, "model": EMBEDDING_MODEL}
