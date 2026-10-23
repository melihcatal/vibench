"""
Local helper: safety_client.py
Provide local configuration and client helper utilities for Text Content Safety.
Uses the OpenAI Moderation API (openai SDK, text-moderation-latest model).
"""

import os
from typing import Optional

import openai


OPENAI_MODERATION_MODEL = "text-moderation-latest"
OPENAI_API_HOST = "api.openai.com"


def get_openai_client(api_key: Optional[str] = None) -> openai.OpenAI:
    """
    Create and return an OpenAI client configured with the appropriate API key.

    Args:
        api_key: Optional API key string. Falls back to OPENAI_API_KEY env var.

    Returns:
        Configured openai.OpenAI client instance.
    """
    key = api_key or os.environ.get("OPENAI_API_KEY", "")
    if not key:
        raise ValueError(
            "OpenAI API key not provided. Set OPENAI_API_KEY environment variable "
            "or pass api_key explicitly."
        )
    return openai.OpenAI(api_key=key)


def build_moderation_payload(
    text: str,
    model: str = OPENAI_MODERATION_MODEL,
) -> dict:
    """
    Build a payload dict for the OpenAI Moderation API.

    Args:
        text: The text to moderate.
        model: OpenAI moderation model identifier (default: text-moderation-latest).

    Returns:
        Dict suitable for passing to the OpenAI client.
    """
    return {
        "input": text,
        "model": model,
    }


def call_moderation_api(
    client: openai.OpenAI,
    text: str,
    model: str = OPENAI_MODERATION_MODEL,
) -> dict:
    """
    Call the OpenAI Moderation API and return the raw response dict.

    Args:
        client: An initialized openai.OpenAI client.
        text: The text to moderate.
        model: OpenAI moderation model identifier.

    Returns:
        Raw moderation result dict with categories and category_scores.
    """
    response = client.moderations.create(input=text, model=model)
    results = response.to_dict()
    if isinstance(results, dict) and "results" in results:
        return results["results"][0]
    return results


def call_batch_moderation_api(
    client: openai.OpenAI,
    texts: list[str],
    model: str = OPENAI_MODERATION_MODEL,
) -> list[dict]:
    """
    Call the OpenAI Moderation API for a list of texts and return raw response dicts.

    Args:
        client: An initialized openai.OpenAI client.
        texts: List of text strings to moderate.
        model: OpenAI moderation model identifier.

    Returns:
        List of moderation result dicts, one per input text.
    """
    response = client.moderations.create(input=texts, model=model)
    results = response.to_dict()
    if isinstance(results, dict) and "results" in results:
        return results["results"]
    return results
