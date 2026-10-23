import os
from typing import List

import dashscope

# Identifier: DashScope Embeddings SDK

dashscope.set_api_key(os.getenv("DASHSCOPE_API_KEY"))


def embed_text(text: str) -> List[float]:
    """Generate embedding for a single text string using DashScope.

    Returns:
        List of float values representing the embedding vector.
    """
    response = dashscope.embeddings.create(
        model="text-embedding-3-large",
        texts=[text],
    )
    # DashScope returns embeddings as a list of lists
    return response.embeddings[0]
