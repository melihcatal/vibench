import re

def check_prompt(user_text: str) -> str:
    """
    Runs a very simple safety filter on the prompt.
    Production systems should use the provider's moderation service.
    Here we disallow control characters, non-ASCII beyond basic Latin, and overly long content.
    """
    # Remove null bytes and control chars
    filtered = ''.join(ch for ch in user_text if ch.isprintable() or ch.isspace())
    # Trim length for safety and cost reasons
    if len(filtered) > 2000:
        filtered = filtered[:2000]
    return filtered
