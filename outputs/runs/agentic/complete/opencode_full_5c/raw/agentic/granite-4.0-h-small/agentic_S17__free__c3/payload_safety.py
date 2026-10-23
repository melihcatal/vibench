# LATER-STEP: payload_safety.py
"""Check decrypted text payloads for unsafe content.

After decryption (using any of the SCORED implementations), this module
analyzes the resulting plaintext for indicators that it may contain
malicious code, privileged data, or other unsafe elements. The approach
uses simple heuristic regexes and a whitelist of allowed characters.

Provider identification: this helper does not directly touch a provider; it
operates on data produced by ``decrypt_payload.py`` or other decryptors.
"""

import re
import json

from security_models import DecryptResponse

# ---------------------------------------------------------------------------
# Unsafe pattern definitions (examples)
# ---------------------------------------------------------------------------
EXECUTABLE_CHARACTERS = re.compile(
    r"[\\`~!@#$%^&*()\-+=\[\]{};:'\\\"\\|,<.>/?]", re.UNICODE
)
# Very simplistic check: presence of shell metacharacters or executable bytes
UNSAFE_REX = [
    EXECUTABLE_CHARACTERS,
    re.compile(r"eval\("),
    re.compile(r"exec\("),
    re.compile(r"system\("),
    re.compile(r"os\.system\("),
]


def _contains_unsafe(text: str) -> bool:
    """Return True if any unsafe pattern matches the supplied text."""
    for pat in UNSAFE_REX:
        if pat.search(text):
            return True
    return False


def check_payload_safety(decrypt_resp: DecryptResponse) -> Dict[str, any]:
    """Analyze a DecryptResponse and return a safety report."""
    plaintext = decrypt_resp.plaintext
    safe = not _contains_unsafe(plaintext)
    report = {
        "key_id": decrypt_resp.key_id,
        "safe": safe,
        "unsafe_reason": None if safe else "Potential unsafe characters detected",
        "provider": "generic-decrypt",  # placeholder; originates from any decryptor
    }
    if not safe:
        report["unsafe_details"] = ", ".join(
            [str(t) for t in UNSAFE_REX if t.search(plaintext)]
        )
    return report


# ---------------------------------------------------------------------------
# CLI helper (optional)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys, json

    if len(sys.argv) != 2:
        print("Usage: python payload_safety.py <decrypt_json_file>")
        sys.exit(1)
    with open(sys.argv[1], "r") as f:
        data = json.load(f)
    resp = DecryptResponse(**data)
    report = check_payload_safety(resp)
    print(json.dumps(report, indent=2))
