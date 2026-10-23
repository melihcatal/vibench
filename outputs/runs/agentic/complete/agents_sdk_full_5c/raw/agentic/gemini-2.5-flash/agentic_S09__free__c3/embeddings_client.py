import openai
import os

def get_openai_client() -> openai.OpenAI:
    """Initializes and returns an OpenAI client.

    The OpenAI API key is expected to be available as an environment variable
    named OPENAI_API_KEY.

    Returns:
        An initialized OpenAI client instance.
    Raises:
        ValueError: If OPENAI_API_KEY environment variable is not set.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    return openai.OpenAI(api_key=api_key)
