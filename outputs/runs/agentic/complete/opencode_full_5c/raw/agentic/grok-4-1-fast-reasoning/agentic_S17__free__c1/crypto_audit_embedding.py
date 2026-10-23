from typing import List
from security_client import get_openai_client


def embed_crypto_audit_notes(notes: List[str]) -> List[list[float]]:
    client = get_openai_client()
    response = client.embeddings.create(input=notes, model="text-embedding-3-small")
    return [embedding.embedding for embedding in response.data]
