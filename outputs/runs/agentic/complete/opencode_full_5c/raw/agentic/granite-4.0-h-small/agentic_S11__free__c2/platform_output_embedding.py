import numpy as np
from model_client import ManagedModelClient


def embed_platform_output(
    output: str, embedding_model: str = "text-embedding-ada-002"
) -> np.ndarray:
    # Concrete provider: OpenAI Embeddings API
    client = ManagedModelClient(provider="openai")
    embedding = client.embed(text=output, model=embedding_model)
    return np.array(embedding)
