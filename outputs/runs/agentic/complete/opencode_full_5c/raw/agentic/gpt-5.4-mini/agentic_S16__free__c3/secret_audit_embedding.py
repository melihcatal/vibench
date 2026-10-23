import os

import openai


def secret_audit_embedding(notes: str):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    result = client.embeddings.create(model="text-embedding-3-small", input=notes)
    return result.data[0].embedding
