# [SAME-SCENARIO] moderate_text.py
"""Scores user text for unsafe or policy-violating content using OpenAI Moderation API."""

from safety_client import get_openai_client


def moderate_text(user_text: str):
    """Return a boolean indicating whether the text is safe."""
    client = get_openai_client()
    response = client.moderations.create(input=user_text)
    # The API returns a list of flagged categories.
    flagged = response["results"][0]["flagged"]
    return not flagged
