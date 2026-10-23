def normalize_request(messages: list[str]) -> dict:
    """Local helper that normalizes list of messages for safety service calls.

    Args:
        messages (list[str]): User messages.

    Returns:
        dict: Normalized payload specific to the provider's request format.
    """
    # Example: simple JSON list format expected by our local helpers
    return {"messages": messages}


def parse_response(raw_response: dict) -> list[dict]:
    """Local helper that parses raw provider response into a standard decision list.

    Args:
        raw_response (dict): Raw response dictionary from provider.

    Returns:
        list[dict]: Standardized moderation decisions.
    """
    decisions = []
    # Generic handling; implement per provider logic elsewhere
    return decisions
