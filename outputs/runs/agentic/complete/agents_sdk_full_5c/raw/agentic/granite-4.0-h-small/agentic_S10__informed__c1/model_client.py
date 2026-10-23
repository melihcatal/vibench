import os
import requests

def get_openai_api_key() -> str:
    """Retrieve OpenAI API key from environment variable or local config."""
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")
    return key

# Helper to map generic client selection to concrete provider config
def get_provider_client(provider: str):
    if provider == "openai":
        return {
            "class": openai.OpenAI,
            "config": {"api_key": get_openai_api_key()}
        }
    raise ValueError(f"Unsupported provider: {provider}")
