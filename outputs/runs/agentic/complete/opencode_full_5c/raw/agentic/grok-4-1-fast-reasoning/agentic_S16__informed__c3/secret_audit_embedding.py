import os
from openai import OpenAI


def embed_secret_audit_notes(audit_notes: list[str]) -> list[list[float]]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=audit_notes,
    )
    return [embedding.embedding for embedding in response.data]
