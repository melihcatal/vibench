from embeddings_client import DirectEmbeddingsClient

# OpenAI Embeddings provider
client = DirectEmbeddingsClient(service="OpenAI")


def embed_text(text: str) -> list[float]:
    """Generate embedding vector for a single text string.

    Args:
        text (str): The input text.
    Returns:
        list[float]: Embedding vector.
    """
    return client.embed(text=text)
