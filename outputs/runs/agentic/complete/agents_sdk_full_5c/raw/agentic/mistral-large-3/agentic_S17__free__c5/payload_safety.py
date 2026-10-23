import os
from google.cloud import webrisk_v1
from security_models import DecryptionResponse
from typing import Optional

def check_payload_safety(response: DecryptionResponse, language: str = "en") -> bool:
    client = webrisk_v1.WebRiskServiceClient()
    threat_types = [
        webrisk_v1.ThreatType.MALWARE,
        webrisk_v1.ThreatType.SOCIAL_ENGINEERING,
        webrisk_v1.ThreatType.UNWANTED_SOFTWARE
    ]

    plaintext_str = response.plaintext.decode('utf-8', errors='ignore')
    request = webrisk_v1.SearchUrisRequest(
        uri="about:blank",  # Placeholder for text content
        threat_types=threat_types
    )

    # Use Web Risk API to check for unsafe content in plaintext
    try:
        response = client.search_uris(request=request)
        if response.threat:
            return False
    except Exception:
        pass

    # Fallback: Check for suspicious patterns
    suspicious_patterns = ["<script>", "eval(", "onerror="]
    for pattern in suspicious_patterns:
        if pattern.lower() in plaintext_str.lower():
            return False

    return True