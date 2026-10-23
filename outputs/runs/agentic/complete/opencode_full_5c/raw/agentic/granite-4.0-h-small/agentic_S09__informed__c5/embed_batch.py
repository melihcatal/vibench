# [SAME-SCENARIO] embed_batch.py
# Generates embeddings for a batch of texts

# Provider: OpenAI Embeddings
# SDK: openai
# Integration signal: OPENAI_API_KEY environment variable

import os
from typing import List
from openai import OpenAI

embeddings_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def embed_batch(texts: List[str]) -> List[list[float]]:
    """Embed a list of texts.
    Returns a list of embedding vectors (one per text).
    """
    response = embeddings_client.embeddings.create(
        model="text-embedding-ada-002",
        input=texts,
    )
    return [item.embedding for item in response.data]
