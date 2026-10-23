import os
from typing import Any

# The concrete provider can be swapped by changing the import and client creation below.
# Here we use OpenAI's Embeddings API as the concrete service.
# Provider identification signal: OPENAI_API_KEY environment variable and openai SDK import.

try:
    import openai
except ImportError:
    raise ImportError('openai SDK not installed. Install via `pip install openai`')


def get_embed_client() -> Any:
    """Return a configured embedding client for the chosen provider.
    Currently configured for OpenAI Embeddings API.
    """
    # Load API key from environment (security best practice)
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise RuntimeError('OPENAI_API_KEY environment variable not set')
    openai.api_key = api_key
    return openai

# Example alternative providers (commented out):
# - DashScope: import dashscope; client = dashscope.embed.Embeddings(...)
# - Cohere: import cohere; client = cohere.Client(...)
# - IBM watsonx.ai: from ibm_watsonx_ai.services import Embeddings; client = Embeddings(...)
