import os, json
import openai

def get_openai_client() -> openai.OpenAI:
    """Return an OpenAI client configured from environment variables."""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise RuntimeError('Set OPENAI_API_KEY environment variable')
    openai.api_key = api_key
    return openai}
