from openai import OpenAI
import os

def embed_audit_notes(notes: str) -> list[float]:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.embeddings.create(
        input=notes,
        model='text-embedding-3-small'
    )
    return response.data[0].embedding
