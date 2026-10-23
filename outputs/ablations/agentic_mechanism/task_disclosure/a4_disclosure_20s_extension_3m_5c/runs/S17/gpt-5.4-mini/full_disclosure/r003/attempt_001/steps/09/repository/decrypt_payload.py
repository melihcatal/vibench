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


def decrypt_payload(ciphertext_b64: str, key_id: Optional[str] = None) -> Dict[str, Any]:
    kms = _kms_client()
    ciphertext = base64.b64decode(ciphertext_b64)
    response = kms.decrypt(CiphertextBlob=ciphertext, KeyId=key_id or os.environ.get(AWS_KMS_KEY_ID_ENV))
    plaintext_bytes = response["Plaintext"]
    plaintext = plaintext_bytes.decode("utf-8")
    return {
        "provider": "aws_kms",
        "key_id": key_id or os.environ.get(AWS_KMS_KEY_ID_ENV),
        "plaintext": plaintext,
        "key_id_returned": response.get("KeyId"),
        "encryption_algorithm": response.get("EncryptionAlgorithm"),
    }


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        return 2
    ciphertext_b64 = argv[1]
    key_id = argv[2] if len(argv) > 2 else None
    result = decrypt_payload(ciphertext_b64, key_id=key_id)
    sys.stdout.write(json.dumps(result, separators=(",", ":")))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
