from openai import OpenAI
import os


def embed_crypto_audit_note(note: str) -> list[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model="text-embedding-3-small", input=note)
    return response.data[0].embedding
