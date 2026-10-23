# [SAME-SCENARIO] moderate_text.py
"""Score user text for unsafe or policy-violating content using Alibaba Cloud Content Moderation SDK."""

from safety_client import get_content_moderation_client


def moderate_text(user_text: str):
    """Return a dict with moderation flags based on Alibaba service."""
    client = get_content_moderation_client()
    response = client.moderate({"text": user_text})
    # Assume response contains 'label' and 'score' fields
    return {
        "label": response.get("label"),
        "score": response.get("score"),
        "service": "Alibaba Content Moderation",
    }
