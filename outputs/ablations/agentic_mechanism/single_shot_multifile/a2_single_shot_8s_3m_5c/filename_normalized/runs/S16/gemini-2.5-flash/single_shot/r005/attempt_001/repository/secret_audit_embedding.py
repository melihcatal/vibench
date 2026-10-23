import os
from typing import List
from security_client import get_openai_client

def embed_audit_notes(notes: List[str]) -> List[List[float]]:
    openai_client = get_openai_client()
    embedding_model = os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

    if not notes:
        return []

    try:
        response = openai_client.embeddings.create(
            input=notes,
            model=embedding_model
        )
        embeddings = [data.embedding for data in response.data]
        return embeddings
    except Exception:
        raise
