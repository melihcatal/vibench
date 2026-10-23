import os
from typing import Any, Dict

# Anthropic SDK (pip install anthropic)
import anthropic

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

client: Any = None

if ANTHROPIC_API_KEY:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
else:
    raise RuntimeError("ANTHROPIC_API_KEY environment variable not set")


def get_llm_client() -> anthropic.Anthropic:
    """Return the configured Anthropic client for hosted LLM calls."""
    global client
    if client is None:
        raise RuntimeError("LLM client not initialized")
    return client

# Optional: add other provider clients here (e.g., watsonx, bedrock) and route based on env vars.
