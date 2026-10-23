import os
from typing import Any

DIRECT_EMBEDDINGS_API_KEY = os.getenv("DIRECT_EMBEDDINGS_API_KEY")
DIRECT_EMBEDDINGS_BASE_URL = os.getenv(
    "DIRECT_EMBEDDINGS_BASE_URL", "https://api.directembeddings.com"
)


def get_client() -> Any:
    """Return a ready‑to‑use client for the Direct Embeddings API.
    The actual client implementation is provider‑specific; here we expose a
    simple wrapper that hides the provider details from higher‑level code.
    """
    try:
        # Example using the official provider SDK (replace with real import)
        from direct_embeddings_sdk import Client
    except ImportError:
        raise RuntimeError("Direct Embeddings SDK not installed")
    return Client(
        api_key=DIRECT_EMBEDDINGS_API_KEY, base_url=DIRECT_EMBEDDINGS_BASE_URL
    )
