import os
from embeddings_client import DirectEmbeddingsConfig

# Configuration
config = DirectEmbeddingsConfig(
    service="DashScope",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="text-embedding-ada-002",
)


def embed_text(text: str) -> list[float]:
    """Generate an embedding vector for a single text string using DashScope Embeddings.

    Args:
        text (str): The input text to embed.

    Returns:
        list[float]: The embedding vector.
    """
    client = config.get_client()
    response = client.embeddings.create(model=config.model, input=text)
    # Assuming the SDK returns a list of floats in response['embedding']
    return response["embedding"]
