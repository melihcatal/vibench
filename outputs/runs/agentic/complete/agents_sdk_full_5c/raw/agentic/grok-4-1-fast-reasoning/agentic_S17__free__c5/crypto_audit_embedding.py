from openai import OpenAI
import os
from typing import List[float]

def embed_crypto_audit_notes(audit_notes: str) -> List[float]:
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    client = OpenAI(api_key=api_key)
    embedding_response = client.embeddings.create(
        input=audit_notes,
        model="text-embedding-3-small"
    )
    return embedding_response.data[0].embedding