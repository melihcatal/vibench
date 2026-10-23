from openai import OpenAI


def secret_audit_embedding(notes: str):
    client = OpenAI()
    result = client.embeddings.create(model="text-embedding-3-small", input=notes)
    return result.data[0].embedding
