import base64
import json
import os
import sys
from typing import Any, Dict, Optional

import boto3


AWS_REGION_ENV = "AWS_REGION"
AWS_KMS_KEY_ID_ENV = "AWS_KMS_KEY_ID"


def _kms_client():
    region = os.environ.get(AWS_REGION_ENV)
    session = boto3.session.Session(region_name=region) if region else boto3.session.Session()
    return session.client("kms")


def encrypt_payload(plaintext: str, key_id: Optional[str] = None) -> Dict[str, Any]:
    kms = _kms_client()
    response = kms.encrypt(KeyId=key_id or os.environ.get(AWS_KMS_KEY_ID_ENV), Plaintext=plaintext.encode("utf-8"))
    ciphertext = response["CiphertextBlob"]
    return {
        "provider": "aws_kms",
        "key_id": key_id or os.environ.get(AWS_KMS_KEY_ID_ENV),
        "ciphertext_b64": base64.b64encode(ciphertext).decode("ascii"),
        "encryption_algorithm": response.get("EncryptionAlgorithm"),
        "key_id_returned": response.get("KeyId"),
    }


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        return 2
    plaintext = argv[1]
    key_id = argv[2] if len(argv) > 2 else None
    result = encrypt_payload(plaintext, key_id=key_id)
    sys.stdout.write(json.dumps(result, separators=(",", ":")))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
