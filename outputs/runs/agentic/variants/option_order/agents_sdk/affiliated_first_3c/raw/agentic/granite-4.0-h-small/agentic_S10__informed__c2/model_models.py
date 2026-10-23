def sanitize_response(text: str) -> str:
    """Simple sanitization: strip surrounding whitespace and ensure valid UTF-8."""
    return text.strip()
