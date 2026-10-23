import os
import cohere

def get_cohere_client():
    """
    Initializes and returns the Cohere client using the API key
    from the environment variables.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")
    
    # Provider-specific client class: cohere.Client
    client = cohere.Client(api_key)
    return client

# Global client instance
cohere_client = get_cohere_client()
