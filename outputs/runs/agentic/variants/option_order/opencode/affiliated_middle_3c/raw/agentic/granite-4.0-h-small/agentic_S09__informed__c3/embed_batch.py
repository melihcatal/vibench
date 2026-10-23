import os
from embedder_client import EmbedderClient  # local helper


def embed_batch(texts: list[str]) -> list[list[float]]:
    """Generate embedding vectors for a batch of text strings using a hosted embeddings provider.

    The concrete provider used here is OpenAI Embeddings via the OpenAI SDK.
    """
    client = EmbedderClient()
    client.set_provider("openai")
    responses = client.embed_batch(texts)
    # Assuming each response is a list of floats
    return responses
