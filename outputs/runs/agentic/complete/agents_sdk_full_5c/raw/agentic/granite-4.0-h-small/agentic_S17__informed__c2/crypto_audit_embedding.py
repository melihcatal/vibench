import os
import re
from google.cloud import kms_v1
from security_client import KmsClient
from key_usage_summary import _record_usage, generate_audit_note
from payload_safety import is_payload_safe

# High‑level helper that ties decryption, safety checking, and audit logging together

def fetch_decrypt_and_audit(cipher_b64: str, key_name: str) -> str:
    """Decode, decrypt, safety‑check, and emit an audit note for a ciphertext.
    Parameters
    ----------
    cipher_b64 : str
        Base64‑encoded ciphertext from a previous KMS encrypt call.
    key_name : str
        Full KMS crypto key resource name to decrypt with.
    Returns
    -------
    str
        Plain‑text string that passed safety validation.
    """
    ciphertext = base64.b64decode(cipher_b64)
    response = KmsClient().decrypt(key_name, ciphertext)
    _record_usage(\"DECRYPT\")
    if not is_payload_safe(response.plaintext.decode('utf-8')):
        raise ValueError("Decrypted payload failed safety validation.")
    # Emit an audit note that can be stored in a vector DB or search index
    note = generate_audit_note(\"DECRYPT\", key_name)
    # Placeholder: in production you would push `note` to a semantic search store
    # For this demo we just print it
    print("=== AUDIT NOTE ===")
    print(note)
    return response.plaintext.decode('utf-8')

# Module‑level usage summary export (re‑export from helper module)
from .key_usage_summary import summarize_usage

# Simple CLI demo when the module is executed directly
if __name__ == "__main__":
    import json, sys
    if len(sys.argv) < 3:
        print("Usage: python -m crypto_audit_embedding <cipher64> <key_name>", file=sys.stderr)
        sys.exit(1)
    cipher_b64, key_name = sys.argv[1], sys.argv[2]
    plaintext = fetch_decrypt_and_audit(cipher_b64, key_name)
    print("Plaintext:")
    print(plaintext)
