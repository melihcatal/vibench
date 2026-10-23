import os
import base64
import logging
from typing import Optional, Dict, List

from security_client import SecurityClient, KMSConfig
from security_models import (
    GenerateDataKeyRequest,
    GenerateDataKeyResponse,
    EnvelopeEncryptResult,
    EncryptRequest,
    EncryptResponse,
    DecryptRequest,
    DecryptResponse,
)

logger = logging.getLogger(__name__)

AWS_KMS_SERVICE = "AWS Key Management Service"
AWS_KMS_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")


def envelope_encrypt(
    plaintext: str,
    key_id: str,
    encryption_context: Optional[Dict[str, str]] = None,
    key_spec: str = "AES_256",
    client: Optional[SecurityClient] = None,
) -> EnvelopeEncryptResult:
    config = KMSConfig.from_env()
    kms_client = client or SecurityClient(config=config)

    data_key_request = GenerateDataKeyRequest(
        key_id=key_id,
        key_spec=key_spec,
        encryption_context=encryption_context,
    )
    data_key_response: GenerateDataKeyResponse = kms_client.generate_data_key(
        data_key_request
    )

    plaintext_bytes = plaintext.encode("utf-8")
    iv, ciphertext_with_tag = SecurityClient.aes_gcm_encrypt(
        plaintext_bytes, data_key_response.plaintext_key_bytes
    )

    ciphertext_blob = base64.b64encode(ciphertext_with_tag).decode("utf-8")
    iv_b64 = base64.b64encode(iv).decode("utf-8")

    result = EnvelopeEncryptResult(
        encrypted_data_key=data_key_response.encrypted_key,
        ciphertext_blob=ciphertext_blob,
        key_id=data_key_response.key_id,
        iv=iv_b64,
        encryption_context=encryption_context,
    )

    logger.info(
        "Envelope encrypted payload with %s CMK %s and local AES-GCM",
        AWS_KMS_SERVICE,
        result.key_id,
    )

    return result


def envelope_decrypt(
    envelope_result: EnvelopeEncryptResult,
    client: Optional[SecurityClient] = None,
) -> str:
    config = KMSConfig.from_env()
    kms_client = client or SecurityClient(config=config)

    decrypt_request = DecryptRequest(
        ciphertext_blob=envelope_result.encrypted_data_key,
        encryption_context=envelope_result.encryption_context,
    )
    decrypt_response: DecryptResponse = kms_client.decrypt(decrypt_request)

    ciphertext_with_tag = base64.b64decode(envelope_result.ciphertext_blob)
    iv = base64.b64decode(envelope_result.iv)

    plaintext_bytes = SecurityClient.aes_gcm_decrypt(
        ciphertext_with_tag, decrypt_response.plaintext_bytes, iv
    )

    logger.info(
        "Envelope decrypted payload with %s CMK %s and local AES-GCM",
        AWS_KMS_SERVICE,
        envelope_result.key_id,
    )

    return plaintext_bytes.decode("utf-8")
