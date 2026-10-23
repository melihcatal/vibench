import openai
import os
from typing import List

def embed_crypto_audit_notes(note: str) -> List[float]:
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    embedding_response = client.embeddings.create(
        model="text-embedding-3-small",
        input=note
    )
    return embedding_response.data[0].embedding