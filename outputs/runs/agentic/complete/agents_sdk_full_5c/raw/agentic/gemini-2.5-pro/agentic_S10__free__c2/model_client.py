import os
import cohere

_client = None

def get_cohere_client():
    """Initializes and returns a singleton Cohere client."""
    global _client
    if _client is None:
        api_key = os.environ.get("COHERE_API_KEY")
        if not api_key:
            raise ValueError("COHERE_API_KEY environment variable not set.")
        _client = cohere.Client(api_key)
    return _client
