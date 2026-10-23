import re
import json
import speech_client


def check_unsafe_content(script: str) -> bool:
    """Simple unsafe content detector using regex patterns.

    Args:
        script (str): Narration script.

    Returns:
        bool: True if unsafe content is detected, False otherwise.
    """
    # Define unsafe patterns (e.g., profanity, personal data placeholders)
    unsafe_patterns = [
        re.compile(r"\b(?:fuck|shit|bitch|asshole)\b", re.IGNORECASE),
        re.compile(r"\b(?:\d{3}-\d{2}-\d{4})\b"),  # Social Security Number pattern
        re.compile(r"\b(?:\d{4}-\d{4}-\d{4}-\d{4})\b"),  # Credit card pattern
        re.compile(r"@example\\.com"),  # Email placeholder
    ]
    for pattern in unsafe_patterns:
        if pattern.search(script):
            return True
    return False
