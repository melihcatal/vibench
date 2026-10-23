import os

from openai import OpenAI


def crypto_audit_embedding(note: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return (
        client.embeddings.create(model="text-embedding-3-small", input=note)
        .data[0]
        .embedding
    )
