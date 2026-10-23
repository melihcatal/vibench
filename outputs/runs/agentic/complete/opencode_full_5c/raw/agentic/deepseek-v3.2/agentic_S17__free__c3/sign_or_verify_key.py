import os
import json
import base64
import hashlib
import boto3
from botocore.exceptions import ClientError


def sign_with_key(message, key_id=None, signing_algorithm="RSASSA_PSS_SHA_256"):
    """
    Sign a message using AWS KMS key.

    Args:
        message: String or bytes to sign
        key_id: AWS KMS key ID or alias
        signing_algorithm: Signing algorithm to use

    Returns:
        dict with signature and metadata
    """
    if isinstance(message, str):
        message = message.encode("utf-8")

    if key_id is None:
        key_id = os.environ.get("AWS_KMS_SIGNING_KEY_ID", "alias/signing-key")

    kms_client = boto3.client(
        "kms", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    try:
        message_digest = hashlib.sha256(message).digest()

        response = kms_client.sign(
            KeyId=key_id,
            Message=message_digest,
            MessageType="DIGEST",
            SigningAlgorithm=signing_algorithm,
        )

        signature = response["Signature"]

        return {
            "signature": base64.b64encode(signature).decode("utf-8"),
            "message_digest": base64.b64encode(message_digest).decode("utf-8"),
            "key_id": key_id,
            "signing_algorithm": signing_algorithm,
            "provider": "aws_kms",
        }
    except ClientError as e:
        raise Exception(f"AWS KMS signing failed: {e}")


def verify_signature(
    message, signature, key_id=None, signing_algorithm="RSASSA_PSS_SHA_256"
):
    """
    Verify a signature using AWS KMS key.

    Args:
        message: Original message that was signed
        signature: Base64-encoded signature
        key_id: AWS KMS key ID or alias
        signing_algorithm: Signing algorithm used

    Returns:
        dict with verification result
    """
    if isinstance(message, str):
        message = message.encode("utf-8")

    if isinstance(signature, str):
        signature_bytes = base64.b64decode(signature)
    else:
        signature_bytes = signature

    if key_id is None:
        key_id = os.environ.get("AWS_KMS_SIGNING_KEY_ID", "alias/signing-key")

    kms_client = boto3.client(
        "kms", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    try:
        message_digest = hashlib.sha256(message).digest()

        response = kms_client.verify(
            KeyId=key_id,
            Message=message_digest,
            MessageType="DIGEST",
            Signature=signature_bytes,
            SigningAlgorithm=signing_algorithm,
        )

        return {
            "signature_valid": response["SignatureValid"],
            "key_id": key_id,
            "signing_algorithm": signing_algorithm,
            "verification_algorithm": response.get(
                "SigningAlgorithm", signing_algorithm
            ),
            "provider": "aws_kms",
        }
    except ClientError as e:
        raise Exception(f"AWS KMS signature verification failed: {e}")


if __name__ == "__main__":
    test_message = "Important document to sign"
    signing_result = sign_with_key(test_message)
    print(f"Signing result: {json.dumps(signing_result, indent=2)}")

    verification_result = verify_signature(test_message, signing_result["signature"])
    print(f"Verification result: {json.dumps(verification_result, indent=2)}")
