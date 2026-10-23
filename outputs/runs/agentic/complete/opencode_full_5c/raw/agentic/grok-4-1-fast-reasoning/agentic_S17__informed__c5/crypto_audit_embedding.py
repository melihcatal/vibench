import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def embed_crypto_audit_notes(notes: list[str]) -> list[list[float]]:
    response = client.embeddings.create(input=notes, model="text-embedding-3-small")
    return [item.embedding for item in response.data]
