# secret_label_safety.py
# Checks secret metadata (labels, descriptions) for unsafe or restricted text.
import re
from safety_client import normalize_secret_payload


def contains_unsafe_text(text: str) -> bool:
    """Simple regex-based scanner for profanity, PII patterns, and other unsafe content."""
    # Example patterns - expand as needed
    patterns = [
        r"\b(pass|secret|token|key)\s*[:=]\s*\w+\b",
        r"\b(?:\d{3}[-.]?\d{2}[-.]?\d{4})\b",  # SSN pattern
        r"\b\d{1,4}[ -]?\d{1,4}[ -]?\d{1,4}[ -]?\d{1,4}\b",  # credit card pattern
        r"@example\\.com",
        r"https?://\\S+",
    ]
    flag = False
    for pat in patterns:
        if re.search(pat, text, re.IGNORECASE):
            flag = True
            break
    return flag


def check_secret_labels(secret: dict) -> bool:
    """Return True if any label/description appears unsafe."""
    # Normalize payload to ensure consistent keys
    norm = normalize_secret_payload(secret)
    # Check description/labels if present
    description = norm.get("description") or norm.get("label")
    if description and contains_unsafe_text(description):
        return True
    return False


if __name__ == "__main__":
    unsafe_example = {
        "username": "admin",
        "password": "Password123",
        "description": "Secret for the admin portal, DO NOT SHARE. P@ssw0rd",
    }
    print(f"Unsafe? {check_secret_labels(unsafe_example)}")
