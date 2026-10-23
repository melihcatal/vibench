import os

from openai import OpenAI


def secret_audit_embedding(notes: str):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(model="text-embedding-3-small", input=notes)
    return response.data[0].embedding
