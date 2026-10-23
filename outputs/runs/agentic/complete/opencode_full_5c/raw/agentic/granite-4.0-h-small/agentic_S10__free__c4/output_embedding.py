import json
import os
from model_client import HostedModelClient
import numpy as np


def embed_output(text: str, model: str = "text-embedding-ada-002") -> np.ndarray:
    """Generates an embedding vector for model output text using a hosted embedding model.

    Args:
        text: The text to embed.
        model: Hosted embedding model identifier.

    Returns:
        Numpy array representing the embedding vector.
    """
    client = HostedModelClient(model=model)
    payload = {
        "text": text,
        "dimensions": 1536,
    }  # Example dimensions for OpenAI embeddings
    response = client.chat_completion(payload)
    embedding_str = response["choices"][0]["message"]["content"]
    try:
        # Assuming the model returns space-separated floats
        vector = np.fromstring(embedding_str, sep=" ")
        return vector
    except Exception as e:
        raise ValueError(f"Failed to parse embedding vector: {e}")
