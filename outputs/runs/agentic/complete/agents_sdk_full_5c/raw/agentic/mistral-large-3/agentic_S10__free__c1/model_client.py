import os
from typing import Optional
from anthropic import Anthropic

_ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")


def get_llm_client() -> Anthropic:
    """
    Return a configured Anthropic client for hosted LLM inference.
    """
    if not _ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required.")
    return Anthropic(api_key=_ANTHROPIC_API_KEY)