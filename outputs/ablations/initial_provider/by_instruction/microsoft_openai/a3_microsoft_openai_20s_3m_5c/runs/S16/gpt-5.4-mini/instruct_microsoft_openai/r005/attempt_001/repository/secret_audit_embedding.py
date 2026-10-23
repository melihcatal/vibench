import os

from openai import OpenAI


def embed_secret_audit_notes(notes: str):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(model="text-embedding-3-large", input=notes)
    return response.data[0].embedding
