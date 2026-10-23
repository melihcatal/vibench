from __future__ import annotations

from security_client import AwsKmsSecurityClient, encode_blob
from security_models import EncryptionRequest, normalize_bytes_payload

AWS_KMS_SERVICE = "AWS Key Management Service"


def encrypt_payload(plaintext, key_id: str, encryption_context=None) -> dict:
    client = AwsKmsSecurityClient()
    request = EncryptionRequest(
        plaintext=normalize_bytes_payload(plaintext),
        key_id=key_id,
        encryption_context=encryption_context,
    )
    response = client.encrypt(request)
    return {
        "service": AWS_KMS_SERVICE,
        "key_id": response.key_id,
        "ciphertext_b64": encode_blob(response.ciphertext),
        "algorithm": response.algorithm,
        "metadata": response.metadata,
    }
