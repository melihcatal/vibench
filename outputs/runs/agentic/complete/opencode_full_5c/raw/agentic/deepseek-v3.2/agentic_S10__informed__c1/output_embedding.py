import os
from openai import OpenAI
from typing import List


def embed_text(text: str) -> List[float]:
    """Embed text using OpenAI embeddings API."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    response = client.embeddings.create(model="text-embedding-3-small", input=text)

    return response.data[0].embedding
