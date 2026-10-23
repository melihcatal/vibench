from openai import OpenAI


def secret_audit_embedding(text: str, model: str = "text-embedding-3-small"):
    client = OpenAI()
    return client.embeddings.create(model=model, input=text).data[0].embedding
