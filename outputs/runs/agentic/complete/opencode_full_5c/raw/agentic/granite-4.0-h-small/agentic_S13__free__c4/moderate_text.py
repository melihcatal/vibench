# SAME-SCENARIO: moderate_text.py
"""Score user text for unsafe or policy‑violating content using OpenAI's moderation endpoint."""

import os
from safety_client import get_moderation_client

API_MODEL = "openai.moderation"  # concrete provider identifier


def moderate_text(user_text: str, threshold: float = 0.5) -> dict:
    """Return a dict with moderation results for a single text.

    Args:
        user_text: The content to evaluate.
        threshold: Score above which content is considered unsafe.

    Returns:
        A dict containing the provider's raw response plus a simple "safe" flag.
    """
    client = get_moderation_client()
    response = client.moderate(text=user_text, model=API_MODEL)
    # Normalize provider response to our internal format
    result = {
        "raw": response,
        "safe": not any(hit["flagged"] for hit in response["results"][0]["categories"]),
    }
    return result
