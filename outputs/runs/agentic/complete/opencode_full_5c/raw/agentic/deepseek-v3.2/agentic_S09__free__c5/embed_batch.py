import os
from openai import OpenAI
from typing import List


def embed_batch(
    texts: List[str], model: str = "text-embedding-3-small"
) -> List[List[float]]:
    """
    Generate embeddings for a batch of texts using OpenAI's embeddings API.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    response = client.embeddings.create(
        model=model, input=texts, encoding_format="float"
    )

    return [item.embedding for item in response.data]
