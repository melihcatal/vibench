"""
[SAME-SCENARIO] moderate_batch.py
Moderates a batch of user messages and returns per-message decisions.
Uses the OpenAI Moderation API via the openai SDK (text-moderation-latest model).
"""

from typing import Optional

from safety_client import get_openai_client, call_batch_moderation_api
from safety_models import (
    BatchModerationResponse,
    ModerationResponse,
    normalize_batch_results,
)


def moderate_batch(
    texts: list[str],
    api_key: Optional[str] = None,
    model: str = "text-moderation-latest",
    batch_size: int = 32,
) -> BatchModerationResponse:
    """
    Moderate a batch of user messages and return per-message decisions
    using the OpenAI Moderation API.

    Args:
        texts: List of user messages to moderate.
        api_key: Optional OpenAI API key. Falls back to OPENAI_API_KEY env var.
        model: OpenAI moderation model identifier (default: text-moderation-latest).
        batch_size: Maximum number of texts per API call (OpenAI limit).

    Returns:
        BatchModerationResponse with one ModerationResponse per input text.
    """
    client = get_openai_client(api_key=api_key)
    all_results: list[ModerationResponse] = []

    for i in range(0, len(texts), batch_size):
        chunk = texts[i : i + batch_size]
        raw_results = call_batch_moderation_api(client, chunk, model=model)
        normalized = normalize_batch_results(raw_results)
        all_results.extend(normalized.results)

    return BatchModerationResponse(results=all_results)


def get_flagged_messages(
    texts: list[str],
    api_key: Optional[str] = None,
    model: str = "text-moderation-latest",
) -> list[tuple[int, str, ModerationResponse]]:
    """
    Return only the flagged messages from a batch with their index, text, and result.

    Args:
        texts: List of user messages.
        api_key: Optional OpenAI API key.
        model: OpenAI moderation model identifier.

    Returns:
        List of (index, text, ModerationResponse) for flagged messages only.
    """
    batch_result = moderate_batch(texts, api_key=api_key, model=model)
    flagged = []
    for idx, response in enumerate(batch_result.results):
        if response.flagged:
            flagged.append((idx, texts[idx], response))
    return flagged


def get_safe_messages(
    texts: list[str],
    api_key: Optional[str] = None,
    model: str = "text-moderation-latest",
) -> list[tuple[int, str]]:
    """
    Return only the safe (non-flagged) messages from a batch.

    Args:
        texts: List of user messages.
        api_key: Optional OpenAI API key.
        model: OpenAI moderation model identifier.

    Returns:
        List of (index, text) for safe messages.
    """
    batch_result = moderate_batch(texts, api_key=api_key, model=model)
    safe = []
    for idx, response in enumerate(batch_result.results):
        if not response.flagged:
            safe.append((idx, texts[idx]))
    return safe
