import base64
import json
import os
from typing import Any, Dict

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


AWS_KMS_KEY_ID_ENV = "AWS_KMS_KEY_ID"
AWS_REGION_ENV = "AWS_REGION"


def _kms_client() -> Any:
    region = os.getenv(AWS_REGION_ENV)
    if region:
        return boto3.client("kms", region_name=region)
    return boto3.client("kms")


def envelope_encrypt(plaintext: bytes) -> Dict[str, str]:
    if not isinstance(plaintext, (bytes, bytearray)):
        raise TypeError("plaintext must be bytes")

    key_id = os.getenv(AWS_KMS_KEY_ID_ENV)
    if not key_id:
        raise ValueError("AWS_KMS_KEY_ID is required")

    kms = _kms_client()
    try:
        response = kms.generate_data_key(KeyId=key_id, KeySpec="AES_256")
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError(f"AWS KMS generate_data_key failed: {exc}") from exc

    data_key_plaintext = response["Plaintext"]
    data_key_ciphertext = response["CiphertextBlob"]

    aesgcm = AESGCM(data_key_plaintext)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, bytes(plaintext), None)

    return {
        "provider": "aws-kms",
        "key_id": key_id,
        "encrypted_data_key": base64.b64encode(data_key_ciphertext).decode("utf-8"),
        "nonce": base64.b64encode(nonce).decode("utf-8"),
        "ciphertext": base64.b64encode(ciphertext).decode("utf-8"),
    }


def main() -> None:
    import sys

    if len(sys.argv) != 2:
        raise SystemExit("usage: envelope_encrypt.py <plaintext>")
    payload = envelope_encrypt(sys.argv[1].encode("utf-8"))
    print(json.dumps(payload))


if __name__ == "__main__":
    main()
