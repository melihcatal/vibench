import os
from typing import List
from openai import OpenAI


def get_embeddings(
    texts: List[str], model: str = "text-embedding-3-small"
) -> List[List[float]]:
    """
    Generates embeddings for a list of texts using OpenAI's API.

    Args:
        texts: A list of strings to embed.
        model: The embedding model to use.

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # OpenAI API recommends replacing newlines with spaces for better performance
    texts = [text.replace("\n", " ") for text in texts]

    response = client.embeddings.create(input=texts, model=model)

    return [embedding.embedding for embedding in response.data]
