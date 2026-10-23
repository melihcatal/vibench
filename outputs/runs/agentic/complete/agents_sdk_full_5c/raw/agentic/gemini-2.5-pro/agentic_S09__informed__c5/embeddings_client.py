import os
import cohere

def get_embeddings_client():
    """
    Returns an initialized Cohere client.
    Expects COHERE_API_KEY environment variable to be set.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")
    
    # Initialize the Cohere client
    # This client can be used for various Cohere API endpoints.
    client = cohere.Client(api_key)
    return client

