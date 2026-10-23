import json
import re

def vendor_text_safety(text: str) -> str:
    """Moderate vendor notes for profanity or PII using a simple regex filter."""
    # Example profanity list (very limited)
    profanity = [r"\b(?:damn|bitch|fuck)\b", r"\b(?:ssn|credit card)\b"]
    for pat in profanity:
        if re.search(pat, text, re.IGNORECASE):
            text = "[CONTENT REMOVED]"
            break
    # Mask SSN-like patterns
    text = re.sub(r"\b\d{3}[- ]?\d{2}[- ]?\d{4}\b", "[SSN REDACTED]", text)
    return text
