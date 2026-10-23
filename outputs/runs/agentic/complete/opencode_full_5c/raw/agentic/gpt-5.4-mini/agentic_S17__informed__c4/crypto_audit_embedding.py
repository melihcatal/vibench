from openai import OpenAI


def crypto_audit_embedding(text: str) -> dict:
    client = OpenAI()
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return {
        "provider": "OpenAI",
        "model": "text-embedding-3-small",
        "embedding": response.data[0].embedding,
    }
