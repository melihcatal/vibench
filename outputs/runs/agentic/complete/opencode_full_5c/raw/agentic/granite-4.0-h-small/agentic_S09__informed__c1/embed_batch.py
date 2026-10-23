# [SAME-SCENARIO] embed_batch.py
# Generates embeddings for a batch of texts using OpenAI Embeddings API

import os
import openai
from typing import List

openai.api_key = os.getenv("OPENAI_API_KEY")


def embed_batch(texts: List[str]) -> List[list[float]]:
    """Embed a list of texts and return a list of embedding vectors.

    Args:
        texts (List[str]): List of text strings to embed.

    Returns:
        List[list[float]]: List of embedding vectors, one per input text.
    """
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=texts,
    )
    # Each entry in 'data' contains an 'embedding' list
    return [item["embedding"] for item in response["data"]]
