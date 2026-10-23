import os
from anthropic import Anthropic

def get_anthropic_client() -> Anthropic:
    """
    Initializes and returns the Anthropic API client.
    
    Expects the ANTHROPIC_API_KEY environment variable to be set.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")
        
    return Anthropic(api_key=api_key)
