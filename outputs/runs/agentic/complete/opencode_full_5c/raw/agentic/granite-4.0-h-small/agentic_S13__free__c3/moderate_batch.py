# [SAME-SCENARIO] moderate_batch.py
"""Moderates a batch of user messages and returns per-message decisions using OpenAI Moderation API."""

from safety_client import get_openai_client


def moderate_batch(messages: list[str]) -> list[bool]:
    """Return a list of booleans indicating safety for each message."""
    client = get_openai_client()
    response = client.moderations.create(input=messages)
    # Each entry corresponds to an input message.
    return [not result["flagged"] for result in response["results"]]
