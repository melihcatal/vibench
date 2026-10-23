import os
from typing import List
from openai import OpenAI

def embed_moderation_rationale(reason: str) -> List[float]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required.")
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(
        input=reason,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding
