import os
from openai import OpenAI


def get_embedding_for_segment(
    text: str, model: str = "text-embedding-3-small"
) -> list[float]:
    """
    Generates an embedding for a text segment using OpenAI's API.

    Args:
        text: The text segment to embed.
        model: The OpenAI embedding model to use.

    Returns:
        A list of floats representing the embedding.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    text = text.replace("\n", " ")

    response = client.embeddings.create(input=[text], model=model)

    return response.data[0].embedding
