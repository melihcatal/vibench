import os
import boto3
from botocore.exceptions import ClientError

# AWS KMS integration (provider-identifying signal)
kms = boto3.client("kms")

KMS_KEY_ID = os.getenv("AWS_KMS_KEY_ID")
if not KMS_KEY_ID:
    raise RuntimeError("AWS_KMS_KEY_ID not set")


def sign_message(message: bytes) -> str:
    """Signs a message using an asymmetric KMS key and returns a base64 encoded signature.

    Returns the signature as a string.
    """
    if not KMS_KEY_ID:
        raise RuntimeError("AWS_KMS_KEY_ID not configured")
    try:
        response = kms.sign(
            KeyId=KMS_KEY_ID,
            Message=message,
            MessageType="RAW",
            Algorithm="RSASSA_PKCS1_V1_5_SHA_256",
        )
        return response["Signature"].decode("utf-8")
    except ClientError as e:
        raise RuntimeError(f"KMS sign failed: {e}")


def verify_signature(message: bytes, signature: str) -> bool:
    """Verifies a signature produced by sign_message using the same KMS key.

    Returns True if verification succeeds.
    """
    if not KMS_KEY_ID:
        raise RuntimeError("AWS_KMS_KEY_ID not set")
    try:
        response = kms.verify(
            KeyId=KMS_KEY_ID,
            Message=message,
            Signature=signature.encode("utf-8"),
            MessageType="RAW",
            Algorithm="RSASSA_PKCS1_V1_5_SHA_256",
        )
        return response["SignatureValid"]
    except ClientError as e:
        raise RuntimeError(f"KMS verify failed: {e}")


# Simple command‑line demo
if __name__ == "__main__":
    test_msg = b"Hello from AWS KMS signing"
    sig = sign_message(test_msg)
    print("Signature:", sig)
    print("Verification:", verify_signature(test_msg, sig))
