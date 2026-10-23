import os
from openai import OpenAI
from typing import List

def get_embedding(text: str) -> List[float]:
    """
    Generates an embedding for a given text using OpenAI's API.

    Args:
        text: The input text to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    # The OpenAI client uses the OPENAI_API_KEY environment variable by default.
    # Provider-specific client class: openai.OpenAI
    client = OpenAI()

    response = client.embeddings.create(
        input=text,
        # Provider-specific model ID: text-embedding-3-small
        model="text-embedding-3-small"
    )

    return response.data[0].embedding
