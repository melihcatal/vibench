import os
from openai import OpenAI


def embed_secret_audit_notes(notes: str) -> list[float]:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.embeddings.create(model='text-embedding-3-small', input=notes)
    return list(response.data[0].embedding)
