import os
from openai import OpenAI


def embed_crypto_audit_note(note: str) -> list[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model="text-embedding-3-small", input=note)
    return [float(x) for x in response.data[0].embedding]
