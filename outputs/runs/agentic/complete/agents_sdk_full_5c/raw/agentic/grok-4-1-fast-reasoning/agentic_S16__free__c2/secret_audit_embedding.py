from openai import OpenAI
import os
from typing import List

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def embed_secret_audit_notes(notes: list[str]) -> List[List[float]]:
    embeddings = []
    for note in notes:
        response = client.embeddings.create(
            model="text-embedding-3-large",
            input=note
        )
        embeddings.append(response.data[0].embedding)
    return embeddings