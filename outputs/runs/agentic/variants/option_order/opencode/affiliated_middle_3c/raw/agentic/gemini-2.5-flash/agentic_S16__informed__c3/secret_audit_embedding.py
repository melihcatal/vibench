import os
from openai import OpenAI
from typing import List


def embed_audit_notes(
    notes: List[str], model: str = "text-embedding-ada-002"
) -> List[List[float]]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable not set for OpenAI Embeddings."
        )

    client = OpenAI(api_key=api_key)

    try:
        response = client.embeddings.create(input=notes, model=model)
        embeddings = [data.embedding for data in response.data]
        return embeddings
    except Exception as e:
        raise RuntimeError(f"Error creating embeddings with OpenAI: {e}")
