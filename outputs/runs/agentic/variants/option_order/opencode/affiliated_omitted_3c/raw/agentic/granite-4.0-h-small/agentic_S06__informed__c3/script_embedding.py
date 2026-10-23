import os
from typing import Any
from dashscope import Embeddings


def embed_narration(script: str, model_id: str = "text-embedding-3-large") -> bytes:
    """Generate an embedding vector for a narration script using DashScope Embeddings.

    Returns the embedding as a binary array (raw bytes). In production you might convert
    to numpy array or store as vector in a database.
    """
    client = Embeddings(api_key=os.getenv("DASHSCOPE_API_KEY"))
    response = client.embeddings(model_id=model_id, input=script)
    # response['embeddings'] is a list of vectors; we return the first one flattened as bytes
    vec = response["embeddings"][0]["vector"]  # list of floats
    return bytes(int(v * 1e5) for v in vec)  # scaled to int bytes for storage


# Example grip (DO NOT commit real API key):
# embedding_bytes = embed_narration("Welcome to the demo!", model_id='text-embedding-3-large')
