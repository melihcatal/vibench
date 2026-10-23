from __future__ import annotations

from typing import Dict, Optional

from security_client import get_kms_client
from security_models import DecryptRequest, DecryptResponse, b64decode_text



def decrypt_payload(
    ciphertext_b64: str,
    encryption_context: Optional[Dict[str, str]] = None,
    region_name: Optional[str] = None,
) -> DecryptResponse:
    request = DecryptRequest(
        ciphertext_b64=ciphertext_b64,
        encryption_context=encryption_context or {},
    )
    kms = get_kms_client(region_name=region_name)
    response = kms.decrypt(
        CiphertextBlob=b64decode_text(request.ciphertext_b64),
        EncryptionContext=request.encryption_context or None,
    )
    plaintext = response["Plaintext"].decode("utf-8")
    return DecryptResponse(
        key_id=response.get("KeyId"),
        plaintext=plaintext,
        metadata={
            "encryption_algorithm": response.get("EncryptionAlgorithm", "SYMMETRIC_DEFAULT"),
            "sdk": "boto3",
            "service": "AWS KMS",
        },
    )
