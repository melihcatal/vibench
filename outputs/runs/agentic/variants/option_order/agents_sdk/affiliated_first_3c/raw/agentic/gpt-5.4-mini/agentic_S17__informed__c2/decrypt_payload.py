from __future__ import annotations

from security_client import AwsKmsSecurityClient, decode_blob
from security_models import DecryptionRequest, normalize_text_payload

AWS_KMS_SERVICE = "AWS Key Management Service"


def decrypt_payload(ciphertext_b64, key_id: str, encryption_context=None) -> dict:
    client = AwsKmsSecurityClient()
    request = DecryptionRequest(
        ciphertext=decode_blob(normalize_text_payload(ciphertext_b64)),
        key_id=key_id,
        encryption_context=encryption_context,
    )
    response = client.decrypt(request)
    return {
        "service": AWS_KMS_SERVICE,
        "key_id": response.key_id,
        "plaintext": response.plaintext.decode("utf-8", errors="replace"),
        "algorithm": response.algorithm,
        "metadata": response.metadata,
    }
