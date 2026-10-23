import openai
import os
from typing import List


def embed_crypto_audit_notes(audit_notes: List[str]) -> List[list]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required.")
    client = openai.OpenAI(api_key=api_key)
    response = client.embeddings.create(
        model="text-embedding-3-small", input=audit_notes
    )
    return [item.embedding for item in response.data]
