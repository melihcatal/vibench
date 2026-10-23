import os
from safety_client import SafetyClient

def moderate_batch(texts: list[str], unsafe_category: str = "harassment") -> list[bool]:
    """Batch moderation using OpenAI's moderation endpoint.

    Args:
        texts: List of user-submitted texts.
        unsafe_category: Safety category to evaluate (default: "harassment").

    Returns:
        List of booleans corresponding to each text, True if unsafe.
    """
    client = SafetyClient()
    # OpenAI moderation supports batch via list of texts
    response = client.moderate(texts=texts)
    # Expected response: list of dicts like moderate_text response
    return [entry.get("categories", {}).get(unsafe_category, False) for entry in response]
