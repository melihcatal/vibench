import os
import json
from security_client import get_aws_kms_client
from security_models import KmsEncryptRequest

# Configure KMS client using AWS credentials
_kms_client = get_aws_kms_client()


def payload_safety(ciphertext: bytes) -> bool:
    """Checks decrypted plaintext for unsafe content (e.g., shell metacharacters)."""
    # Placeholder implementation: return True if safe, False otherwise
    # In a real deployment you might run a content moderation API or regex check
    # For demo purposes, assume any non‑empty binary payload is safe
    return bool(ciphertext)


if __name__ == "__main__":
    # Example of decrypting then safety‑checking (for testing only)
    from encrypt_payload import encrypt_payload, decrypt_payload

    msg = b"Hello, world!"
    enc = encrypt_payload(msg, os.getenv("AWS_KMS_KEY_ID"))
    dec = decrypt_payload(enc["CiphertextBlob"], os.getenv("AWS_KMS_KEY_ID"))
    print("Plaintext safe?", payload_safety(dec["Plaintext"]))
