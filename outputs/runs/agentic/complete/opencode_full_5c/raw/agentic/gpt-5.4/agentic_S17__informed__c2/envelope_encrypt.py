from __future__ import annotations

from typing import Dict, Optional

from security_client import (
    aesgcm_encrypt,
    encode_b64,
    get_kms_client,
    get_kms_key_id,
    kms_context,
)
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse


def envelope_encrypt(
    plaintext: str,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
) -> Dict[str, object]:
    request = EnvelopeEncryptionRequest(
        plaintext=plaintext,
        key_id=key_id,
        encryption_context=kms_context(encryption_context),
    )
    kms_client = get_kms_client()
    generated = kms_client.generate_data_key(
        KeyId=get_kms_key_id(request.key_id),
        KeySpec="AES_256",
        EncryptionContext=request.encryption_context,
    )
    encrypted_payload = aesgcm_encrypt(
        request.plaintext.encode("utf-8"), generated["Plaintext"]
    )
    response = EnvelopeEncryptionResponse(
        ciphertext=encrypted_payload["ciphertext"],
        encrypted_data_key=encode_b64(generated["CiphertextBlob"]),
        key_id=generated["KeyId"],
        algorithm="AES_256_GCM",
        metadata={
            "nonce": encrypted_payload["nonce"],
            "kms_keyspec": generated.get("KeySpec"),
            "kms_provider": "AWS KMS",
        },
    )
    return response.to_dict()
