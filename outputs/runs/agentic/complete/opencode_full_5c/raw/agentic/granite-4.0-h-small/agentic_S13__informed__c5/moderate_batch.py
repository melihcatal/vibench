# moderate_batch.py

import os
from safety_client import TextSafetyClient


def moderate_batch(messages: list[str]) -> list[dict]:
    """Moderate a batch of user messages and return per‑message decisions.
    Uses ibm‑watsonx‑ai Guardrails (Hate, Abuse, and Profanity detection).
    Returns a list of dicts, one per message, containing the provider response.
    """
    client = TextSafetyClient()
    responses = client.batch_analyze(messages=messages)
    return responses
