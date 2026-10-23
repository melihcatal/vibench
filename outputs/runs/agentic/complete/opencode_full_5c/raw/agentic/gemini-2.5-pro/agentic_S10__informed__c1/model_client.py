import os
import openai


def get_openai_client() -> openai.OpenAI:
    """
    Initializes and returns the OpenAI client using the API key
    from the environment.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    return openai.OpenAI(api_key=api_key)
