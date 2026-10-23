import re

# Simple profanity filter placeholder - replace with a real moderation API (e.g., Perspective API)
def vendor_text_safety(text: str) -> bool:
    """Return False if the vendor note contains disallowed language, else True."""
    # Example regex filter for common profanity
    profanity_pattern = re.compile(r"\b(?:badword1|badword2|badword3)\b", re.IGNORECASE)
    if profanity_pattern.search(text):
        return False
    return True