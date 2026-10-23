import os
import base64
from .security_client import kms_decrypt
from .security_models import DecryptionRequest, DecryptionResponse

# Decrypt Payload (Same-scenario)


def decrypt_payload(req: DecryptionRequest) -> DecryptionResponse:
    """
    Decrypts ciphertext that was previously encrypted with an AWS KMS managed key.
    Returns the recovered plaintext as bytes.
    """
    return {
        "plaintext": kms_decrypt(base64.b64decode(req["ciphertext"]), req["key_id"])
    }


# Additional helper for envelope decryption


def envelope_decrypt(encrypted_data_key: str, ciphertext: str, key_id: str) -> bytes:
    """
    Decrypts an envelope-encrypted payload:
    1. Decrypt the encrypted data key with the KMS managed key.
    2. Use the plaintext data key to decrypt the ciphertext.
    Returns the original plaintext bytes.
    """
    edk_bytes = base64.b64decode(encrypted_data_key)
    data_key = kms_decrypt(edk_bytes, key_id)  # decrypt the envelope key
    return kms_decrypt(base64.b64decode(ciphertext), data_key["KeyId"])
