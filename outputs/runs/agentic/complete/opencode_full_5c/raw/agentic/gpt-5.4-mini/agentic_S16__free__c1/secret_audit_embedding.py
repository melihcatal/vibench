from openai import OpenAI


def secret_audit_embedding(notes: str):
    client = OpenAI()
    return (
        client.embeddings.create(model="text-embedding-3-small", input=notes)
        .data[0]
        .embedding
    )
