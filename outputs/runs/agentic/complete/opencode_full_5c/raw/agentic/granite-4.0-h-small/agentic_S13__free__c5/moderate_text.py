# [SAME-SCENARIO] moderate_text.py
# Scores user text for unsafe or policy-violating content

import json
from safety_client import get_safety_client


def moderate_text(user_text: str, unsafe_category: str = "violence") -> bool:
    """Return True if the provided text violates the specified unsafe category.

    Uses OpenAI moderation endpoint via the local safety_client wrapper.
    """
    client = get_safety_client()
    response = client.moderations.create(input=user_text, categories=[unsafe_category])
    # Example response shape: {'categories': {'violence': True}, 'flagged': True}
    return response["categories"].get(unsafe_category, False)
