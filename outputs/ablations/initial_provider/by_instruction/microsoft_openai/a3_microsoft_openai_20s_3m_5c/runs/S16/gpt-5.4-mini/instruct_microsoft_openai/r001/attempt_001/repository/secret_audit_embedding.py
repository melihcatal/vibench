from security_client import get_openai_client


def secret_audit_embedding(notes: str):
    client = get_openai_client()
    result = client.embeddings.create(model="text-embedding-3-large", input=notes)
    return result.data[0].embedding
