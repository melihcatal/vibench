import os
from openai import OpenAI
from typing import List

def embed_secret_audit_notes(audit_notes: str) -> List[float]:
    api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=audit_notes
    )
    return response.data[0].embedding