import os
from embedder_client import EmbedderClient  # local helper


def embed_text(text: str) -> list[float]:
    """Generate an embedding vector for a single text string using a hosted embeddings provider.

    The concrete provider used here is OpenAI Embeddings via the OpenAI SDK.
    """
    client = EmbedderClient()
    # OpenAI provider identifiers
    client.set_provider("openai")
    response = client.embed(text)
    # Assuming response is a list of floats representing the embedding vector
    return response
