import openai
import os
from typing import List


def embed_crypto_audit_notes(notes: str) -> List[float]:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model="text-embedding-3-small", input=notes)
    return response.data[0].embedding
