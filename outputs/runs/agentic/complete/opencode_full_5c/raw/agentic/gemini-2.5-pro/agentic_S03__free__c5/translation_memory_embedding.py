from typing import List
from translation_client import get_openai_client


def get_embedding(text: str) -> List[float]:
    """
    Generates a vector embedding for a text segment using OpenAI's API.

    Args:
        text: The text to embed.

    Returns:
        A list of floats representing the vector embedding.
    """
    client = get_openai_client()
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=[text], model="text-embedding-3-small")
    return response.data[0].embedding
