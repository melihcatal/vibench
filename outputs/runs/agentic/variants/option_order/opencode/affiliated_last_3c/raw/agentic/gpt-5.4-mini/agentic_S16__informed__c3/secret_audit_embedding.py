from openai import OpenAI


def secret_audit_embedding(text: str):
    client = OpenAI()
    return (
        client.embeddings.create(model="text-embedding-3-small", input=text)
        .data[0]
        .embedding
    )
