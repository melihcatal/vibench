# [LATER-STEP] payload_safety.py
import json
import re
import html

# Helper to detect unsafe content in decrypted payloads


def detect_unsafe_content(text: str) -> dict:
    """Scans plaintext for potentially unsafe indicators and returns a safety report.

    Returns a dict with booleans for each check and a short human‑readable note.
    """
    # Simple regex checks for common unsafe artefacts
    unsafe_patterns = [
        re.compile(r"<script.*?>.*?</script>", re.IGNORECASE | re.DOTALL),
        re.compile(r"javascript:\w+"),
        re.compile(r"data:\s*text/html"),
    ]
    report = {
        "contains_script": False,
        "contains_javascript_url": False,
        "contains_data_uri_html": False,
        "note": "Clean",
    }
    for pat in unsafe_patterns:
        if pat.search(text):
            report["contains_script"] = True
            report["note"] = "Potentially unsafe content detected"
            break
    # Also check for common malicious encodings (e.g., HTML entities)
    decoded = html.unescape(text)
    if decoded != text:
        report["note"] = "Decoded HTML entities present"
    return report
