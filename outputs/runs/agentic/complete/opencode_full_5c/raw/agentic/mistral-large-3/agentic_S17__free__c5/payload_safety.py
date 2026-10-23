import os
import json
from typing import Dict, Any
import requests


def check_payload_safety(
    plaintext: str, context: Dict[str, Any] = None
) -> Dict[str, Any]:
    api_key = os.getenv("GOOGLE_CLOUD_WEB_RISK_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_CLOUD_WEB_RISK_API_KEY environment variable not set")

    url = "https://webrisk.googleapis.com/v1/uris:search"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    # Check for URLs in plaintext
    payload = {
        "uri": f"http://example.com/{plaintext}",  # Dummy URI to leverage Web Risk API
        "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"],
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    threats = response.json().get("threat", {})
    is_unsafe = any(threats.values())

    # Check for sensitive data patterns
    sensitive_patterns = {
        "credit_card": r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9]{2})[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})\b",
        "ssn": r"\b(?!000|666|9\d{2})\d{3}-(?!00)\d{2}-(?!0000)\d{4}\b",
        "api_key": r"\b(AIza[0-9A-Za-z-_]{35}|ya29\.[0-9A-Za-z-_]+)\b",
    }

    pattern_matches = {}
    for pattern_name, pattern in sensitive_patterns.items():
        import re

        if re.search(pattern, plaintext):
            pattern_matches[pattern_name] = True
            is_unsafe = True
        else:
            pattern_matches[pattern_name] = False

    return {
        "is_unsafe": is_unsafe,
        "threats": threats,
        "sensitive_data_matches": pattern_matches,
        "key_id": context.get("key_id") if context else None,
        "algorithm": context.get("algorithm") if context else None,
    }
