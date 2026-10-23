import os
from openai import OpenAI

def embed_text(text: str) -> list[float]:
    """
    Embeds platform outputs for evaluation or retrieval using OpenAI.

    Args:
        text: The text to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    # The OpenAI client reads the OPENAI_API_KEY from environment variables by default.
    # Provider-specific client class
    client = OpenAI()

    response = client.embeddings.create(
        input=text,
        # Provider-specific model ID
        model="text-embedding-3-small"
    )

    return response.data[0].embedding
