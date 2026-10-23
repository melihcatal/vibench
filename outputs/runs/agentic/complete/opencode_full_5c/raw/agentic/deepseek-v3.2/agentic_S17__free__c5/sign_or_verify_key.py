import os
import base64
import hashlib
import boto3
from botocore.exceptions import ClientError


def sign_with_key(
    message: str, key_id: str = None, signing_algorithm: str = "RSASSA_PSS_SHA_256"
) -> dict:
    """
    Sign a message using AWS KMS asymmetric key.

    Args:
        message: The message to sign
        key_id: AWS KMS key ID or alias
        signing_algorithm: Signing algorithm to use

    Returns:
        Dictionary with signature and metadata
    """
    if key_id is None:
        key_id = os.getenv("AWS_KMS_SIGNING_KEY_ID", "alias/signing-key")

    kms_client = boto3.client("kms", region_name=os.getenv("AWS_REGION", "us-east-1"))

    # Hash the message
    message_hash = hashlib.sha256(message.encode("utf-8")).digest()

    try:
        response = kms_client.sign(
            KeyId=key_id,
            Message=message_hash,
            MessageType="DIGEST",
            SigningAlgorithm=signing_algorithm,
        )

        signature = base64.b64encode(response["Signature"]).decode("utf-8")

        return {
            "signature": signature,
            "key_id": key_id,
            "signing_algorithm": signing_algorithm,
            "message_digest": base64.b64encode(message_hash).decode("utf-8"),
            "provider": "aws_kms",
        }
    except ClientError as e:
        raise Exception(f"AWS KMS signing failed: {e}")


def verify_signature(
    message: str,
    signature: str,
    key_id: str = None,
    signing_algorithm: str = "RSASSA_PSS_SHA_256",
) -> bool:
    """
    Verify a signature using AWS KMS asymmetric key.

    Args:
        message: The original message
        signature: Base64-encoded signature
        key_id: AWS KMS key ID or alias
        signing_algorithm: Signing algorithm used

    Returns:
        True if signature is valid, False otherwise
    """
    if key_id is None:
        key_id = os.getenv("AWS_KMS_SIGNING_KEY_ID", "alias/signing-key")

    kms_client = boto3.client("kms", region_name=os.getenv("AWS_REGION", "us-east-1"))

    # Hash the message
    message_hash = hashlib.sha256(message.encode("utf-8")).digest()
    signature_bytes = base64.b64decode(signature)

    try:
        response = kms_client.verify(
            KeyId=key_id,
            Message=message_hash,
            MessageType="DIGEST",
            Signature=signature_bytes,
            SigningAlgorithm=signing_algorithm,
        )

        return response["SignatureValid"]
    except ClientError as e:
        raise Exception(f"AWS KMS verification failed: {e}")


if __name__ == "__main__":
    test_message = "Important document to sign"

    # Sign the message
    signature_result = sign_with_key(test_message)
    print(f"Signature result: {signature_result}")

    # Verify the signature
    is_valid = verify_signature(test_message, signature_result["signature"])
    print(f"Signature valid: {is_valid}")

    # Test with tampered message
    is_valid_tampered = verify_signature(
        "Tampered message", signature_result["signature"]
    )
    print(f"Tampered signature valid: {is_valid_tampered}")
