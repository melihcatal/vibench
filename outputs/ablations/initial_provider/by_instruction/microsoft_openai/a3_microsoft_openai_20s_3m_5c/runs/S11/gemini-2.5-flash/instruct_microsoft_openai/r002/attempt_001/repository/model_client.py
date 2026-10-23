import os
from openai import OpenAI

def get_openai_client() -> OpenAI:
    """
    Provides local configuration and client helper utilities for Managed Model Platform Workflow.
    Returns an initialized OpenAI client.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    base_url = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    return OpenAI(
        api_key=api_key,
        base_url=base_url
    )
