import os
from safety_client import SafetyClient

def moderate_text(user_text: str, unsafe_category: str = "harassment") -> bool:
    """Determine if a single piece of text violates safety policy using OpenAI's moderation endpoint.

    Args:
        user_text: The text submitted by a user.
        unsafe_category: The specific safety category to check (default: "harassment").

    Returns:
        True if the text is flagged as unsafe for the given category; False otherwise.
    """
    client = SafetyClient()
    response = client.moderate(text=user_text)
    # Assume response format: { "flagged": bool, "categories": { category: bool, ... } }
    return response.get("categories", {}).get(unsafe_category, False)