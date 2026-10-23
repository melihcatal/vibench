import os
from typing import Any

# Provider selection via environment variable (example: OPENAI_API_KEY for OpenAI)
PROVIDER = os.getenv('EMBEDDINGS_PROVIDER', 'openai').lower()

def get_embedding_client() -> Any:
    """Instantiate and return a provider-specific embedding client.
    Currently supports OpenAI embeddings as an example concrete provider.
    """
    if PROVIDER == 'openai':
        import openai
        openai.api_key = os.getenv('OPENAI_API_KEY')
        return openai
    else:
        raise ValueError(f'Unsupported provider: {PROVIDER}')
