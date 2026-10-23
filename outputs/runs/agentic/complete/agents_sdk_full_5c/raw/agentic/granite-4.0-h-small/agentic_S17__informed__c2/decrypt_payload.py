import os
import base64
import re
from google.cloud import kms_v1
from security_client import KmsClient
from key_usage_summary import _record_usage

# Public helper that actually performs the decryption after usage logging
# This is the function exposed by the external package and called from other modules.

def decrypt_payload(ciphertext_b64: str, key_name: str) -> str:
    """Decrypt ciphertext using KMS and return plaintext string.
    Parameters
    ----------
    ciphertext_b64 : str
        Base64-encoded ciphertext produced by a KMS Encrypt call.
    key_name : str
        Full KMS resource name of the crypto key (e.g., projects/.../keys/...).
    Returns
    -------
    str
        Plaintext decoded as UTF-8.
    """
    ciphertext = base64.b64decode(ciphertext_b64)
    response = KmsClient().decrypt(key_name, ciphertext)
    _record_usage(\"DECRYPT\")
    # Strip PKCS7 padding if present (demo only)
    plaintext_bytes = response.plaintext
    plaintext = plaintext_bytes.decode('utf-8')
    return plaintext

# Expose usage summary for callers
from .key_usage_summary import summarize_usage

# Keep import order clean; the module can be used as:
#   from decrypt_payload import decrypt_payload, summarize_usage

if __name__ == "__main__":
    # Tiny demo when run directly: expect JSON from stdin {\"cipher\":...,\"key\":...}
    import json, sys
    data = json.load(sys.stdin)
    print(decrypt_payload(data[\"cipher\"], data[\"key\"]))
