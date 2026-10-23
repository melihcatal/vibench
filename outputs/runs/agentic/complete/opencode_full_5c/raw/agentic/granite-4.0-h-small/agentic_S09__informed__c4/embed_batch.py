from embeddings_client import DirectEmbeddingsClient

# OpenAI Embeddings provider
client = DirectEmbeddingsClient(service="OpenAI")


def embed_batch(texts: list[str]) -> list[list[float]]:
    """Generate embedding vectors for a batch of texts.

    Args:
        texts (list[str]): List of input texts.
    Returns:
        list[list[float]]: List of embedding vectors.
    """
    return client.embed_batch(texts=texts)
