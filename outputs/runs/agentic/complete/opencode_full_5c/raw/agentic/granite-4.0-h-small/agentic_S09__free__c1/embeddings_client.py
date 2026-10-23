# [HELPER] embeddings_client.py
# Local configuration and client utilities for Direct Embeddings API

import os
from openai import OpenAI


def get_openai_client() -> OpenAI:
    """Return an OpenAI client configured with env vars or explicit API key."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Set OPENAI_API_KEY environment variable")
    return OpenAI(api_key=api_key)
