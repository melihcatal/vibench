import os
from openai import OpenAI
from typing import List


def embed_text(text: str, model: str = "text-embedding-3-small") -> List[float]:
    """
    Generate an embedding vector for one text string using OpenAI's embeddings API.

    Args:
        text: The text string to embed
        model: The OpenAI embedding model to use (default: text-embedding-3-small)

    Returns:
        List[float]: The embedding vector
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    response = client.embeddings.create(
        model=model, input=text, encoding_format="float"
    )

    return response.data[0].embedding
