import base64
import json
import os
from typing import Any, Dict, Optional

import boto3


def encrypt_payload(plaintext: str, key_id: Optional[str] = None, region_name: Optional[str] = None) -> Dict[str, Any]:
    kms = boto3.client("kms", region_name=region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))
    response = kms.encrypt(KeyId=key_id or os.environ["AWS_KMS_KEY_ID"], Plaintext=plaintext.encode("utf-8"))
    ciphertext_blob = response["CiphertextBlob"]
    return {
        "provider": "aws_kms",
        "key_id": key_id or os.environ["AWS_KMS_KEY_ID"],
        "ciphertext_blob_b64": base64.b64encode(ciphertext_blob).decode("ascii"),
        "encryption_algorithm": response.get("EncryptionAlgorithm"),
        "arn": response.get("KeyId"),
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Encrypt a plaintext payload with AWS KMS.")
    parser.add_argument("plaintext")
    parser.add_argument("--key-id", dest="key_id")
    parser.add_argument("--region", dest="region_name")
    args = parser.parse_args()
    print(json.dumps(encrypt_payload(args.plaintext, args.key_id, args.region_name)))


if __name__ == "__main__":
    main()
