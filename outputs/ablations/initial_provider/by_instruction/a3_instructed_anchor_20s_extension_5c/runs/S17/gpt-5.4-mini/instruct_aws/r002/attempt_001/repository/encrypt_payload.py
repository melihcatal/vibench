from __future__ import annotations

from security_client import get_kms_key_id, kms_client
from security_models import PayloadEnvelope, bytes_to_b64, normalize_text


def encrypt_payload(plaintext: str, key_id: str | None = None) -> dict:
    client = kms_client()
    response = client.encrypt(KeyId=key_id or get_kms_key_id(), Plaintext=normalize_text(plaintext).encode("utf-8"))
    envelope = PayloadEnvelope(
        plaintext=normalize_text(plaintext),
        ciphertext_blob_b64=bytes_to_b64(response["CiphertextBlob"]),
        key_id=response.get("KeyId") or key_id or get_kms_key_id(),
    )
    return envelope.to_dict()
