import os
from safety_client import SafetyClient


def moderate_text(user_text: str) -> bool:
    """Score user text for unsafe or policy-violating content.

    Returns True if unsafe, False otherwise.
    """
    client = SafetyClient()
    response = client.moderate(user_text)
    return response["unsafe"]
