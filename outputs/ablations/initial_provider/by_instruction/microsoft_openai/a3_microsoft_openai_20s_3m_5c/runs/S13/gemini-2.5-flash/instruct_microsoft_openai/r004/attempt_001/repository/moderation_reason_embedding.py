import os
from typing import List
from openai import OpenAI

def embed_moderation_rationale(rationale: str) -> List[float]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    if not client.api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set.")

    try:
        response = client.embeddings.create(
            input=rationale,
            model="text-embedding-ada-002"
        )
        return response.data[0].embedding
    except Exception as e:
        raise RuntimeError(f"Error generating embedding: {e}")
