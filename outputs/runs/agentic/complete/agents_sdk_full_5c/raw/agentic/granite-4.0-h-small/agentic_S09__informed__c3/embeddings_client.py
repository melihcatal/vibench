import os
import openai

def get_embed_client() -> openai.OpenAI:
    """Return a configured OpenAI client for embeddings.
    The client credentials are read from environment variables.
    Provider: OpenAI (OpenAI Embeddings) – identifiable by the `openai` SDK import and `openai.OpenAI` class.
    """
    # Ensure the API key is available
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise RuntimeError('Set OPENAI_API_KEY environment variable for Direct Embeddings')
    openai.api_key = api_key
    return openai.OpenAI()
