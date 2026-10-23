import json
import re
from typing import Any

# Local helper import for controlled environment
from security_client import KeyManagementClient
from security_models import PlaintextPayload

# Pattern to detect unsafe content (example: XSS, SQLi, JavaScript, sensitive patterns)
UNSAFE_RE = re.compile(
    r"(<script.*?>.*?</script>)|"          # inline script tags
    r"(on\w+=\".*?")|"                  # event handlers
    r"(javascript:\")|"                # data: URI schemes
    r"(--|/*\*.*?\*/)|"                  # SQL comment markers
    r"(union.*?select)|"                # common SQLi
    r"(xp_cmdshell)|"                  # SQL extended procs
    r"(eval\(.*?\))"                    # JavaScript eval exec
    , re.IGNORECASE
)

def check_payload(payload: str) -> bool:
    """Return True if payload contains unsafe constructs, False otherwise."""
    return bool(UNSAFE_RE.search(payload))

# Wrapper that raises an exception for unsafe payloads
def validate_payload(payload: PlaintextPayload) -> None:
    if check_payload(payload["plaintext"]):
        raise RuntimeError("Payload contains unsafe content detected by safety scanner.")

# Example integration with decryption workflow
if __name__ == "__main__":
    # Assume a decrypted payload returned from decrypt_payload.py (represented as dict)
    decrypted: PlaintextPayload = {
        "plaintext": "User input: <script>alert('XSS')</script> -- DROP TABLE users;"
    }
    validate_payload(decrypted)
    print("Payload passed safety check")
