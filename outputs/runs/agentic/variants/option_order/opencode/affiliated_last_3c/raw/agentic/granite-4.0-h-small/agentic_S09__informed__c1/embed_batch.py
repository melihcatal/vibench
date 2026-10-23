import os
from embeddings_client import DirectEmbeddingsConfig
from typing import List

# Configuration
config = DirectEmbeddingsConfig(
    service="DashScope",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="text-embedding-ada-002",
)


def embed_batch(texts: List[str]) -> List[list[float]]:
    """Generate embeddings for a batch of texts using DashScope Embeddings.

    Args:
        texts (List[str]): List of texts to embed.

    Returns:
        List[list[float]]: List of embedding vectors for each text.
    """
    client = config.get_client()
    response = client.embeddings.create(model=config.model, input=texts)
    return response["embeddings"]
