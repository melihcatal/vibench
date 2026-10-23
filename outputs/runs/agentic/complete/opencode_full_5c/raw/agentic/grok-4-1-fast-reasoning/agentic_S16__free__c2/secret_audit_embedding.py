import os
from openai import OpenAI


def embed_audit_notes(audit_notes: str) -> list[float]:
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = openai_client.embeddings.create(
        input=audit_notes, model="text-embedding-3-small"
    )
    return response.data[0].embedding
