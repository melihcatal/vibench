import os
from typing import Dict, Any

import ibm_watsonx_ai  # IBM watsonx.ai SDK for Direct Embeddings API

# Configuration via environment variables
WATSONX_API_KEY = os.getenv('WATSONX_API_KEY')
WATSONX_PROJECT_ID = os.getenv('WATSONX_PROJECT_ID')
if not WATSONX_API_KEY or not WATSONX_PROJECT_ID:
    raise RuntimeError('Set WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables')

watsonx.api_key = WATSONX_API_KEY
watsonx.project_id = WATSONX_PROJECT_ID

_default_client = None

def get_embedder() -> Any:
    """Lazy-load an IBM watsonx.ai text embedding client.

    Returns:
        A client with an `embed` method that returns raw embedding data.
    """
    global _default_client
    if _default_client is None:
        from ibm_watsonx_ai.services import TextEmbeddingService
        _default_client = TextEmbeddingService()
    return _default_client


def embed_text(text: str) -> Dict[str, Any]:
    """Embed a single document using watsonx.ai.

    Returns raw response (includes 'embedding' list under 'result').
    """
    return get_embedder().embed(text=text)


def embed_batch(texts: list[str]) -> Dict[str, Any]:
    """Embed multiple documents using watsonx.ai.

    Returns raw response (list of embedding results under 'results').
    """
    return get_embedder().batch_embed(texts=texts)
