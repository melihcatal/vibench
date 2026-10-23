import openai
import os

def get_openai_client():
    """Returns an initialized OpenAI client."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    openai.api_key = api_key
    return openai

def get_embedding_model_name():
    """Returns the default embedding model name."""
    return "text-embedding-ada-002"
