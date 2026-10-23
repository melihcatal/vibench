# [HELPER] embeddings_client.py
# Local configuration and client helper utilities for Direct Embeddings API

import os
from typing import Optional

# Provider: OpenAI Embeddings (using openai SDK)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY environment variable not set")

# Simple singleton client
_openai_client = None


def get_openai_client() -> "openai.OpenAI":
    """Return a configured OpenAI client; lazily initializes once."""
    global _openai_client
    if _openai_client is None:
        import openai

        _openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
    return _openai_client


# Example helper to embed a single text using the configured client
def embed(text: str) -> list[float]:
    """Embed a single text using the helper client."""
    resp = get_openai_client().embeddings.create(
        model="text-embedding-ada-002",
        input=text,
    )
    return resp["data"][0]["embedding"]
