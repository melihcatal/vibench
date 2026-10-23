import os
from typing import List
from openai import OpenAI


def embed_batch(
    texts: List[str], model: str = "text-embedding-3-small"
) -> List[List[float]]:
    """
    Generate embeddings for a batch of texts using OpenAI's embeddings API.

    Args:
        texts: List of text strings to embed
        model: The embedding model to use (default: text-embedding-3-small)

    Returns:
        List of embedding vectors, one for each input text
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    response = client.embeddings.create(model=model, input=texts)

    return [item.embedding for item in response.data]
