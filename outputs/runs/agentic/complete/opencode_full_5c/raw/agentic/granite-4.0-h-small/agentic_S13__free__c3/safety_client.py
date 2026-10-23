# [HELPER] safety_client.py
"""Local configuration and client helper utilities for Text Content Safety.
Uses OpenAI Moderation API as the concrete provider.
"""

import os
from openai import OpenAI


def get_openai_client() -> OpenAI:
    """Return an OpenAI client configured with environment credentials."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")
    return OpenAI(api_key=api_key)


# Example helper to normalize request payload (optional)


def build_moderation_payload(text: str) -> dict:
    """Prepare payload for OpenAI moderation request."""
    return {"input": text}
