import re

# [LATER-STEP] message_safety.py
# Check message payload text for unsafe content using a simple regex filter

UNSAFE_PATTERNS = [
    r"http[s]?://",  # URLs
    r"www\\.",  # www. strings
    r"\\b(?:sex|porn|drugs)\\b",  # offensive words (example list)
]


def is_unsafe(message_body: dict) -> bool:
    """Return True if the message payload contains unsafe content."""
    content = str(message_body.get("content", ""))
    for pattern in UNSAFE_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            return True
    return False
