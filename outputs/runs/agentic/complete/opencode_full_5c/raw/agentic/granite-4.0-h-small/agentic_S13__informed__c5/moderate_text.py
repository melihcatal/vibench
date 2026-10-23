# moderate_text.py

import os
from safety_client import TextSafetyClient


def moderate_text(user_text: str) -> dict:
    """Score a single piece of user text for unsafe or policy‑violating content.
    Uses ibm‑watsonx‑ai Guardrails (Hate, Abuse, and Profanity detection).
    Returns a dict with the provider‑specific response.
    """
    client = TextSafetyClient()
    response = client.analyze(text=user_text)
    return response
