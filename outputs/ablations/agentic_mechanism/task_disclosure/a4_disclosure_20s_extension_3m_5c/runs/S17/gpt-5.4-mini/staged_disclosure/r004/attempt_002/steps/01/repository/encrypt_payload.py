import os
import base64
from typing import Optional

import boto3


def encrypt_payload(plaintext: str, key_id: Optional[str] = None) -> str:
    kms_key_id = key_id or os.environ["AWS_KMS_KEY_ID"]
    kms = boto3.client("kms")
    response = kms.encrypt(KeyId=kms_key_id, Plaintext=plaintext.encode("utf-8"))
    return base64.b64encode(response["CiphertextBlob"]).decode("utf-8")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("Usage: encrypt_payload.py <plaintext> [kms_key_id]")
    payload = sys.argv[1]
    key = sys.argv[2] if len(sys.argv) > 2 else None
    print(encrypt_payload(payload, key))
