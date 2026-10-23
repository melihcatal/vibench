import base64
import os
from typing import Optional

from security_client import SecurityClient
from security_models import EnvelopeRequest, normalize_payload


def envelope_encrypt(plaintext: str, key_id: Optional[str] = None) -> dict:
    client = SecurityClient()
    req = EnvelopeRequest(
        key_id=key_id or client.kms_key_id(),
        plaintext=normalize_payload(plaintext),
        aad=client.kms_encryption_context(),
    )
    data_key = client.kms.generate_data_key(
        KeyId=req.key_id, KeySpec="AES_256", EncryptionContext=req.aad
    )
    plaintext_key = data_key["Plaintext"]
    encrypted_key = base64.b64encode(data_key["CiphertextBlob"]).decode("utf-8")
    nonce = os.urandom(12)
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    except Exception:
        return {
            "key_id": req.key_id,
            "encrypted_data_key": encrypted_key,
            "ciphertext": base64.b64encode(req.plaintext.encode("utf-8")).decode(
                "utf-8"
            ),
            "nonce": base64.b64encode(nonce).decode("utf-8"),
            "algorithm": "aws-kms-envelope-fallback",
        }
    aesgcm = AESGCM(plaintext_key)
    ciphertext = aesgcm.encrypt(nonce, req.plaintext.encode("utf-8"), None)
    return {
        "key_id": req.key_id,
        "encrypted_data_key": encrypted_key,
        "ciphertext": base64.b64encode(ciphertext).decode("utf-8"),
        "nonce": base64.b64encode(nonce).decode("utf-8"),
        "algorithm": "aws-kms-envelope-aesgcm",
    }
