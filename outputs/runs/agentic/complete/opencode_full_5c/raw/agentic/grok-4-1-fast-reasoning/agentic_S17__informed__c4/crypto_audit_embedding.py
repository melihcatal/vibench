import os
from openai import OpenAI
from typing import List, str


def embed_crypto_audit_notes(notes: List[str]) -> List[list[float]]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(input=notes, model="text-embedding-3-small")
    return [emb.embedding for emb in response.data]
