import os
from google.cloud import storage
import re
from security_models import DecryptRequest

# Simple safety check for decrypted payloads
# This is a placeholder basic content safety filter

SAFE_PATTERN = re.compile(r"(^|\s)(password|secret|api key|token)(\s|$)", re.IGNORECASE)


def payload_safety_check(decrypted: DecryptRequest) -> bool:
    """Return True if decrypted text appears unsafe (contains common secrets)."""
    # Split on whitespace and check each word
    words = decrypted["plaintext"].split()
    for w in words:
        if SAFE_PATTERN.search(w):
            return False
    return True


if __name__ == "__main__":
    encrypted_msg = os.getenv("ENCRYPTED_PAYLOAD", "secret password here")
    result = payload_safety_check(
        {"plaintext": encrypted_msg, "status": {"code": 0, "message": "ok"}}
    )
    print("Payload safe?", result)
