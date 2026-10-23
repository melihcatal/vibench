# embed_text.py - SAME-SCENARIO
# Generates an embedding vector for a single text string using DashScope Embeddings

import os
import dashscope

# Load API key from environment
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
if not DASHSCOPE_API_KEY:
    raise ValueError("Set DASHSCOPE_API_KEY environment variable")

dashscope.api_key = DASHSCOPE_API_KEY


def embed_text(text: str) -> list:
    """Return a list of floats representing the embedding of the input text.

    Args:
        text (str): The text to embed.

    Returns:
        list: Embedding vector as a list of floats.
    """
    response = dashscope.embeddings.create(
        model="text-embedding-003",  # concrete model identifier
        texts=[text],
    )
    # response['embeddings'][0]['data'] contains the vector list
    return response["embeddings"][0]["data"]
