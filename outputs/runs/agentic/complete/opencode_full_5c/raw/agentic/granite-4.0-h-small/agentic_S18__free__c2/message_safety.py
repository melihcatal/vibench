import re
from typing import List, Dict


def is_unsafe(text: str) -> bool:
    """Basic regex‑based content safety check (e.g., profanity filters)."""
    # Example patterns: profanity, email addresses, URLs
    patterns = [
        r"\b(?:fuck|shit|bitch|asshole)\b",
        r"\bhttps?://\S+\b",
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}\b",
    ]
    for pat in patterns:
        if re.search(pat, text, flags=re.IGNORECASE):
            return True
    return False


def scan_messages(messages: List[Dict[str, any]]) -> List[Dict[str, any]]:
    """Flag unsafe messages and return a summary dict."""
    unsafe = []
    for msg in messages:
        content = msg.get("payload") or str(msg)
        if is_unsafe(content):
            unsafe.append({"id": msg.get("id"), "reason": "unsafe content"})
    return unsafe
