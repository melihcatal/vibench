import base64
import json
import re
from typing import List, Dict, Tuple
from .security_client import get_security_config


def is_sensitive(text: str) -> bool:
    # Simple heuristic: looks for typical PII patterns
    patterns = [
        r"\b(?:\+?\d{1,3}[- ]?)?(?:\(??\d{3}\)?[- ]?)\d{3}[- ]?\d{4}\b",  # phone numbers
        r"\b[0-9]{3}-[0-9]{2}-[0-9]{4}\b",  # SSN (US)
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # emails
    ]
    for p in patterns:
        if re.search(p, text):
            return True
    return False


def check_decrypted_payload(payload: str) -> Dict[str, List[str]]:
    # Provider‑agnostic safety check (no outbound call)
    issues: List[str] = []
    if is_sensitive(payload):
        issues.append("Contains potential personal or sensitive data")
    if payload.startswith("http://") or payload.startswith("https://"):
        issues.append("Starts with a URL – could be an external link")
    if len(payload) > 2000:
        issues.append("Payload exceeds 2000 characters")
    return {"safe": not bool(issues), "issues": issues}


if __name__ == "__main__":
    # Expect JSON via stdin: {"ciphertext": "", "plaintext": ""}
    raw = sys.stdin.read()
    data = json.loads(raw)
    plaintext = data.get("plaintext", "")
    result = check_decrypted_payload(plaintext)
    # Produce a small safety JSON for downstream processes
    output = json.dumps(result, indent=2)
    print(output)
