import os
from openai import OpenAI
from typing import List

def embed_crypto_audit_notes(audit_notes: str) -> List[float]:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.embeddings.create(
        input=audit_notes,
        model="text-embedding-3-small"
    )
    return [float(val) for val in response.data[0].embedding]