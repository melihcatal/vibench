import os
import cohere


def get_cohere_client():
    """Initializes and returns a Cohere client."""
    cohere_api_key = os.environ.get("COHERE_API_KEY")
    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")
    return cohere.Client(cohere_api_key)
