import json
from safety_check import check_unsafe_text
from security_client import get_kms_client

def decrypt_and_check(ciphertext_b64: str, key_name: str) -> dict:
    """Decrypt payload and evaluate for unsafe content using WatsonX Guardrails.",
    "Provider marker: the safety_check module abstracts WatsonX Guardrails client.",
    """
    plaintext = decrypt_payload(ciphertext_b64, key_name)
    unsafe, issues = check_unsafe_text(plaintext)
    return {
        "decrypted": plaintext,
        "unsafe": unsafe,
        "issues": issues if unsafe else []
    }

# CLI demo
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: payload_safety.py <ciphertext_b64> <key_name>")
        sys.exit(1)
    report = decrypt_and_check(sys.argv[1], sys.argv[2])
    print(json.dumps(report, indent=2))

# Provider import hidden inside safety_check.check_unsafe_text
try:
    from safety_check import check_unsafe_text
except ImportError:
    def check_unsafe_text(text: str):
        """Placeholder that flags a few dangerous words.",
        """ dangerous = {'secret', 'password', 'token', 'ssh', 'key'}
        issues = [w for w in text.lower().split() if w in dangerous]
        return bool(issues), issues
