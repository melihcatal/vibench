from __future__ import annotations

from security_client import kms_client
from security_models import PayloadEnvelope, b64_to_bytes, normalize_text


def decrypt_payload(ciphertext_blob_b64: str, plaintext_hint: str = "") -> dict:
    client = kms_client()
    response = client.decrypt(CiphertextBlob=b64_to_bytes(ciphertext_blob_b64))
    plaintext = response["Plaintext"].decode("utf-8", errors="replace")
    return PayloadEnvelope(plaintext=normalize_text(plaintext_hint) or plaintext, ciphertext_blob_b64=ciphertext_blob_b64, key_id=response.get("KeyId")).to_dict()
