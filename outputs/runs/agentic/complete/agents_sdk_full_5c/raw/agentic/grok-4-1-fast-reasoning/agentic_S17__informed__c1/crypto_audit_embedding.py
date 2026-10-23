from openai import OpenAI
import os

def embed_crypto_audit_notes(audit_notes: list[str]) -> list[list[float]]:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.embeddings.create(
        input=audit_notes,
        model="text-embedding-3-small"
    )
    return [data.embedding for data in response.data]