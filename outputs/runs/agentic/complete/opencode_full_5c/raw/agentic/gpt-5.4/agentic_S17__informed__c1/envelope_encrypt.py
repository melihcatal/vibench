from __future__ import annotations

from typing import Dict, Optional
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from security_client import (
    AWS_KMS_PROVIDER,
    get_kms_client,
    normalize_encryption_context,
)
from security_models import EnvelopeEncryptRequest, EnvelopeEncryptResult, encode_bytes


def envelope_encrypt(
    key_id: str,
    plaintext: str,
    encryption_context: Optional[Dict[str, str]] = None,
    region_name: Optional[str] = None,
    data_key_spec: str = "AES_256",
) -> Dict[str, object]:
    request = EnvelopeEncryptRequest(
        key_id=key_id,
        plaintext=plaintext,
        encryption_context=normalize_encryption_context(encryption_context),
        data_key_spec=data_key_spec,
    )
    client = get_kms_client(region_name)
    data_key_response = client.generate_data_key(
        KeyId=request.key_id,
        KeySpec=request.data_key_spec,
        EncryptionContext=request.encryption_context,
    )
    plaintext_key = data_key_response["Plaintext"]
    wrapped_key = data_key_response["CiphertextBlob"]
    nonce = os.urandom(12)
    aesgcm = AESGCM(plaintext_key)
    ciphertext_with_tag = aesgcm.encrypt(nonce, request.plaintext.encode("utf-8"), None)
    ciphertext = ciphertext_with_tag[:-16]
    tag = ciphertext_with_tag[-16:]
    result = EnvelopeEncryptResult(
        provider=AWS_KMS_PROVIDER,
        key_id=data_key_response["KeyId"],
        wrapped_data_key=encode_bytes(wrapped_key),
        ciphertext=encode_bytes(ciphertext),
        nonce=encode_bytes(nonce),
        tag=encode_bytes(tag),
        algorithm="AES-256-GCM via AWS KMS GenerateDataKey",
        encryption_context=request.encryption_context,
    )
    return result.to_dict()
