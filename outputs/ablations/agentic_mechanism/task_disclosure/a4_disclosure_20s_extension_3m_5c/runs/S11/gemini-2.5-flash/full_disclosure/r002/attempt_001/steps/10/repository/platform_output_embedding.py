import os
from openai import OpenAI

def embed_platform_output(text: str) -> list[float]:
    """
    Embeds platform outputs using OpenAI's embedding model.

    Args:
        text: The text to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(
        input=[text],
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

