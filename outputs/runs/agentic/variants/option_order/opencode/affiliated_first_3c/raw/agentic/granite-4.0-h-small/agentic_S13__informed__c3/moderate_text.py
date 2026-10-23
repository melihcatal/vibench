# [SAME-SCENARIO] moderate_text.py

import os
from safety_client import TextSafetyClient


def score_text(text: str) -> dict:
    """Score user text using the configured safety client and return the provider response."""
    client = TextSafetyClient()
    return client.analyze(text)
