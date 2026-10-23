# payload_safety.py
import re
from typing import List

def contains_unsafe_content(text: str) -> bool:
    """Very simple heuristic to flag unsafe payloads.

    Flags:
        - Presence of private data patterns (credit card, SSN, email)
        - Prompts for malicious instructions
    Returns True if unsafe, False otherwise.
    """
    patterns = [
        r'\b(?:\d[ -]*?){13,16}\b',  # simple credit card pattern
        r'\b\d{3}-\d{2}-\d{4}\b',   # SSN pattern
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}\b',  # email addresses (often unwanted in raw outputs)
        r'(?:show me how to|write a script to|give me a command to)\s*(?:exploit|hack|bypass|malware|virus|trojan)',  # malicious intent
    ]
    for pat in patterns:
        if re.search(pat, text, re.IGNORECASE):
            return True
    return False

def sanitize_payload(text: str) -> str:
    """Attempts to redact sensitive patterns from the text.

    Returns the redacted string or the original if no changes needed.
    """
    return re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[REDACTED-SSN]', text)
