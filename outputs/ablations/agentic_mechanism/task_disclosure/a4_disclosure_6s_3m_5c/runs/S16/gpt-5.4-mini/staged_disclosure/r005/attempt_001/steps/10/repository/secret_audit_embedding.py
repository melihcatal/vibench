import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def embed_secret_audit_notes(notes):
    response = client.embeddings.create(model="text-embedding-3-small", input=notes)
    return [item.embedding for item in response.data]
