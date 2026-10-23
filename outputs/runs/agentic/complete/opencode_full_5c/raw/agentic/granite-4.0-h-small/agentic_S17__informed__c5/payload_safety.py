# payload_safety.py
# Check decrypted plaintext payloads for unsafe or malicious content

import os
import requests
from typing import Any, Dict

# Provider: watsonx.ai guardrails / HAP detection (watsonx)
# Expected env vars: WATSONX_API_KEY, WATSONX_PROJECT_ID

WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
if not WATSONX_API_KEY or not WATSONX_PROJECT_ID:
    raise RuntimeError("Set WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables")

guardrails_endpoint = "https://api.watsonx.ibm.com/guardrails/v1/detect"

def is_payload_safe(plaintext: str) -> bool:
    """Send plaintext to watsonx guardrails and return True if no unsafe content is detected."""
    payload = {
        "content": [plaintext]  # Each entry is a string; batch allowed
    }
    headers = {
        "Authorization": f"Bearer {WATSONX_API_KEY}",
        "Content-Type": "application/json"
    }
    resp = requests.post(guardrails_endpoint, json=payload, headers=headers)
    resp.raise_for_status()
    result = resp.json()
    # Guardrails returns a list of issues under \"issues\"; empty list => safe
    return len(result.get("issues", [])) == 0

# Example CLI helper
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: payload_safety.py <plaintext>\", file=sys.stderr)
        sys.exit(1)
    plain = sys.argv[1]
    safe = is_payload_safe(plain)
    print(f"Payload safe? {safe}")
