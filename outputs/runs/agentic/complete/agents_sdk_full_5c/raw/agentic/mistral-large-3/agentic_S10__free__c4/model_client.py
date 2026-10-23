import os
from openai import OpenAI
from typing import Optional


def get_llm_client() -> OpenAI:
    """
    Initialize and return an OpenAI client using the API key from environment.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    return OpenAI(api_key=api_key)


def get_model_family(model: Optional[str] = None) -> str:
    """
    Return the model family for a given model identifier.
    """
    if not model:
        return "gpt-4o"
    if model.startswith("gpt-4"):
        return "gpt-4"
    elif model.startswith("gpt-3.5"):
        return "gpt-3.5"
    else:
        return "unknown"