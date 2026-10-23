import os
from openai import OpenAI


def embed_secret_audit_notes(audit_notes: str) -> list[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    embedding = client.embeddings.create(
        model="text-embedding-3-small", input=audit_notes
    )
    return embedding.data[0].embedding
