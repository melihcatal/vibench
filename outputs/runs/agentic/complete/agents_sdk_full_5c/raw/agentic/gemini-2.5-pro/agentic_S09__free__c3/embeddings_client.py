import os
import cohere

def get_cohere_client():
    """
    Initializes and returns the Cohere client using an API key
    from the environment variables.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")
    
    client = cohere.Client(api_key)
    return client
