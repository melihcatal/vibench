from __future__ import annotations

from typing import Dict, Optional

from security_client import get_kms_client
from security_models import EncryptRequest, EncryptResponse, b64encode_bytes, normalize_text_payload



def encrypt_payload(
    key_id: str,
    plaintext: str,
    encryption_context: Optional[Dict[str, str]] = None,
    region_name: Optional[str] = None,
) -> EncryptResponse:
    request = EncryptRequest(
        key_id=key_id,
        plaintext=normalize_text_payload(plaintext),
        encryption_context=encryption_context or {},
    )
    kms = get_kms_client(region_name=region_name)
    response = kms.encrypt(
        KeyId=request.key_id,
        Plaintext=request.plaintext.encode("utf-8"),
        EncryptionContext=request.encryption_context or None,
    )
    return EncryptResponse(
        key_id=request.key_id,
        ciphertext_b64=b64encode_bytes(response["CiphertextBlob"]),
        algorithm=response.get("EncryptionAlgorithm", "SYMMETRIC_DEFAULT"),
        metadata={
            "aws_account_id": response.get("KeyId", ""),
            "sdk": "boto3",
            "service": "AWS KMS",
        },
    )
