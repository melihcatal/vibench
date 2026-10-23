import json
import os

import boto3

from security_client import require_key_id


def sign_or_verify_key(message: str, signature: str = None, key_id: str = None):
    kms = boto3.client(
        "kms", region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    )
    key_id = key_id or require_key_id()
    if signature is None:
        result = kms.sign(
            KeyId=key_id,
            Message=message.encode("utf-8"),
            MessageType="RAW",
            SigningAlgorithm="RSASSA_PSS_SHA_256",
        )
        return {
            "key_id": key_id,
            "signature": result["Signature"].hex(),
            "algorithm": "AWS KMS sign",
        }
    result = kms.verify(
        KeyId=key_id,
        Message=message.encode("utf-8"),
        MessageType="RAW",
        Signature=bytes.fromhex(signature),
        SigningAlgorithm="RSASSA_PSS_SHA_256",
    )
    return {
        "key_id": key_id,
        "valid": result["SignatureValid"],
        "algorithm": "AWS KMS verify",
    }


if __name__ == "__main__":
    print(json.dumps(sign_or_verify_key("hello")))
