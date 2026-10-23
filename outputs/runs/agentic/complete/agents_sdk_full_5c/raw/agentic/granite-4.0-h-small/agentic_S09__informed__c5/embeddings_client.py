# embeddings_client.py
# HELPER
import os
import openai


def get_embed_client() -> openai.Embedding:
    """Return an OpenAI Embedding client configured from environment variables."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Set OPENAI_API_KEY environment variable")
    openai.api_key = api_key
    return openai.Embedding
