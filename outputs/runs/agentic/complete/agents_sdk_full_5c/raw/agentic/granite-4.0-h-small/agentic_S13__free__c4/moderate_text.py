# moderate_text.py
"""Scores a single user text for unsafe or policy-violating content using OpenAI's content filter.
"""
import os
from safety_client import OpenAIContentSafetyClient

def moderate_text(user_text: str) -> dict:
    """Return a dictionary with moderation decision.
    {
        "passed": bool,
        "flagged_categories": List[str],
        "detail": Optional[str]
    }"""
    client = OpenAIContentSafetyClient()
    response = client.moderate([user_text])
    # Assume response format: [{"results": [{"flagged_categories": [...], "flagged": True/False, "detail": ...}]}]
    result = response[0]["results"][0]
    return {
        "passed": not result["flagged"],
        "flagged_categories": result["flagged_categories"],
        "detail": result.get("detail")
    }
