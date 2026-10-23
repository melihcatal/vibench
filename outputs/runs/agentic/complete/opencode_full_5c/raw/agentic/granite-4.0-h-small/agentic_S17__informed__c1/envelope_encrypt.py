import os
import base64
from .security_client import envelope_encrypt
from .security_models import EncryptionRequest

# Envelope Encryption (Same-scenario)


def envelope_encrypt(req: EncryptionRequest) -> dict:
    """
    Demonstrates envelope encryption using AWS KMS.
    Returns a dict containing the encrypted data key and the ciphertext.
    """
    return envelope_encrypt(req["plaintext"], req["key_id"])


# Optional: signing & verification using KMS
from .security_client import sign_key, verify_key


def sign_or_verify_key(action: str, key_id: str, data: bytes) -> bytes | bool:
    """
    Generic helper for signing or verification where the KMS supports asymmetric keys.
    Action should be 'sign' or 'verify'.
    Returns the signature (bytes) for 'sign' or a bool for 'verify'.
    """
    if action == "sign":
        return sign_key(key_id, data)
    elif action == "verify":
        # verify expects signature as bytes, returns bool
        signature = base64.b64decode(data)  # assume caller provides base64 sig
        return verify_key(key_id, signature, data)
    else:
        raise ValueError("Unsupported action")
