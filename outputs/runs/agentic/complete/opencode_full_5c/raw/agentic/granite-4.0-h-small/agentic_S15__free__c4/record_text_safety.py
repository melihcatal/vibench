# [LATER-STEP] record_text_safety.py
"""Utility to check document fields for unsafe user‑generated text.

Uses a simple heuristic: flags any field containing suspicious keywords or
URL schemes. In a production system, replace this with a proper content‑moderation
API (e.g., AWS Comprehend, OpenAI Moderation, ContentSafety service). The
implementation demonstrates where such a provider would be integrated.
"""

from typing import Any, Dict, List

SUSPICIOUS_KEYWORDS = [
    "hack",
    "phish",
    "virus",
    "malware",
    "exploit",
    "spam",
    "malicious",
    "illegal",
    "adult",
    "nudity",
    "profane",
    "offensive",
]
URL_SCHEMES = ["http://", "https://", "ftp://"]


def is_text_safe(document: Dict[str, Any], field_names: List[str]) -> bool:
    """Return True if all supplied fields in the document are safe.

    A field is considered unsafe if:
    1. It contains any of the SUSPICIOUS_KEYWORDS (case‑insensitive).
    2. It contains a URL with a disallowed scheme in URL_SCHEMES.
    """
    for field in field_names:
        value = document.get(field)
        if not isinstance(value, str):
            continue
        lower = value.lower()
        # Check for keywords
        for kw in SUSPICIOUS_KEYWORDS:
            if kw in lower:
                return False
        # Check for disallowed URL schemes
        for scheme in URL_SCHEMES:
            if value.startswith(scheme):
                return False
    return True
