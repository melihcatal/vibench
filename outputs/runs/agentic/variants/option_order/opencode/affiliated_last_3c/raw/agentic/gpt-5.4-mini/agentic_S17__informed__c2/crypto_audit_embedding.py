import os

from openai import OpenAI


def crypto_audit_embedding(text: str) -> list[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    result = client.embeddings.create(model="text-embedding-3-small", input=text)
    return result.data[0].embedding
