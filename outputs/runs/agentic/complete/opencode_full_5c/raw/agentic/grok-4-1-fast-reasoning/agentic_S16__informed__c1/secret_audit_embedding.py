import os
from openai import OpenAI


def secret_audit_embedding(audit_notes: str) -> list[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        input=audit_notes, model="text-embedding-3-small"
    )
    return [emb for emb in response.data[0].embedding]
