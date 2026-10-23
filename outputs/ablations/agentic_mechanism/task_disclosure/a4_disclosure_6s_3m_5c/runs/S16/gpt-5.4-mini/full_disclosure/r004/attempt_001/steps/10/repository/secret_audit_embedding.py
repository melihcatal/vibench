import os
from typing import List, Sequence

from openai import OpenAI


def embed_secret_audit_notes(notes: Sequence[str]) -> List[List[float]]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model="text-embedding-3-small", input=list(notes))
    return [item.embedding for item in response.data]
