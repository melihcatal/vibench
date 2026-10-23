# HELPER: Local configuration and client utilities for Text Content Safety

import os
import openai  # Concrete provider: OpenAI

API_KEY = os.getenv("OPENAI_API_KEY")


def get_client() -> openai.OpenAI:
    """Return a configured OpenAI client that uses the moderation endpoint."""
    if not API_KEY:
        raise RuntimeError("Set OPENAI_API_KEY environment variable")
    return openai.OpenAI(api_key=API_KEY)
