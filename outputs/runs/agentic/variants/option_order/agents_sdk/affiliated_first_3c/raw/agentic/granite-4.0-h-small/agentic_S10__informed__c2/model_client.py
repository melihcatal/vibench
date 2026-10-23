import os
from openai import OpenAI

def get_llm_client() -> OpenAI:
    """Return a configured OpenAI client using environment variables.\n    Requires OPENAI_API_KEY to be set.\n    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")
    return OpenAI(api_key=api_key)
