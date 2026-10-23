from __future__ import annotations

import base64
import os
from typing import Any, Dict

import boto3

from security_client import get_aws_kms_client
from security_models import CryptoRequest, CryptoResponse, normalize_text_payload


def envelope_encrypt(request: CryptoRequest) -> CryptoResponse:
    kms = get_aws_kms_client(region=os.getenv("AWS_REGION"))
    data_key = kms.generate_data_key(KeyId=request.key_name, KeySpec="AES_256")
    plaintext = normalize_text_payload(request.plaintext).encode("utf-8")
    key_bytes = data_key["Plaintext"]
    encrypted = bytes(b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(plaintext))
    payload = base64.b64encode(encrypted).decode("ascii")
    metadata: Dict[str, Any] = {
        "provider": "aws-kms",
        "encrypted_data_key": base64.b64encode(data_key["CiphertextBlob"]).decode("ascii"),
    }
    return CryptoResponse(key_name=request.key_name, operation="envelope_encrypt", payload=payload, metadata=metadata)


if __name__ == "__main__":
    pass
