# [HELPER] safety_client.py
# Local configuration and client helper utilities for Text Content Safety

import os
import openai

# Load API key from environment (or local .env)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Identify the concrete provider we are using
PROVIDER = "openai"

# Simple wrapper with a single entry point
_client = None


def get_safety_client() -> openai.OpenAI:
    """Return a singleton OpenAI client instance."""
    global _client
    if _client is None:
        _client = openai.OpenAI()
    return _client


# Example usage inside other files:
# client = get_safety_client()
# client.moderations.create(...)
