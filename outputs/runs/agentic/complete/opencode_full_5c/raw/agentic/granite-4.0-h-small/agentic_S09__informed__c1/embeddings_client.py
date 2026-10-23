# [HELPER] embeddings_client.py
# Local helper utilities for Direct Embeddings API

import os
import openai
from typing import List

# Configure OpenAI client with API key from env
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_client() -> openai.OpenAI:
    """Return a configured OpenAI client instance."""
    return openai


def embed_texts(texts: List[str]) -> List[list[float]]:
    """Embed a list of strings using OpenAI's embedding endpoint."""
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=texts,
    )
    # Extract embedding vectors from response
    return [item["embedding"] for item in response["data"]]
