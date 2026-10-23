import os

from openai import OpenAI


def secret_audit_embedding(text: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return (
        client.embeddings.create(model="text-embedding-3-small", input=text)
        .data[0]
        .embedding
    )
