import base64
import os
from typing import Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


def _b64decode(value: str) -> bytes:
    return base64.b64decode(value.encode("utf-8"))


def _b64encode(value: bytes) -> str:
    return base64.b64encode(value).decode("utf-8")


def sign_message(key_id: str, message: bytes, message_type: str = "RAW") -> str:
    client = boto3.client("kms")
    response = client.sign(
        KeyId=key_id,
        Message=message,
        MessageType=message_type,
        SigningAlgorithm="RSASSA_PSS_SHA_256",
    )
    return _b64encode(response["Signature"])


def verify_signature(key_id: str, message: bytes, signature_b64: str, message_type: str = "RAW") -> bool:
    client = boto3.client("kms")
    try:
        response = client.verify(
            KeyId=key_id,
            Message=message,
            MessageType=message_type,
            Signature=_b64decode(signature_b64),
            SigningAlgorithm="RSASSA_PSS_SHA_256",
        )
        return bool(response.get("SignatureValid", False))
    except (BotoCoreError, ClientError):
        return False


def main() -> None:
    key_id = os.environ.get("AWS_KMS_KEY_ID")
    if not key_id:
        raise SystemExit("AWS_KMS_KEY_ID is required")

    mode = os.environ.get("MODE", "sign").lower()
    message = os.environ.get("MESSAGE", "hello").encode("utf-8")

    if mode == "sign":
        print(sign_message(key_id, message))
        return

    signature_b64 = os.environ.get("SIGNATURE_B64")
    if not signature_b64:
        raise SystemExit("SIGNATURE_B64 is required for verification")
    print("true" if verify_signature(key_id, message, signature_b64) else "false")


if __name__ == "__main__":
    main()
