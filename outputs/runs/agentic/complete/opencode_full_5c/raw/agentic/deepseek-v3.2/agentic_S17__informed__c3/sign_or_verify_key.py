import os
import hashlib
from security_client import get_kms_client
from security_models import SignRequest, VerifyRequest, SignResponse, VerifyResponse


def sign_payload(message: str, key_id: str) -> SignResponse:
    """Sign a message using AWS KMS."""
    client = get_kms_client()

    try:
        # Hash the message
        message_digest = hashlib.sha256(message.encode("utf-8")).digest()

        response = client.sign(
            KeyId=key_id,
            Message=message_digest,
            MessageType="DIGEST",
            SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA_256",
        )

        signature = response["Signature"]

        return SignResponse(
            success=True,
            signature=signature,
            key_id=key_id,
            algorithm="RSASSA_PKCS1_V1_5_SHA_256",
            provider="aws_kms",
        )
    except Exception as e:
        return SignResponse(success=False, error=str(e), provider="aws_kms")


def verify_signature(message: str, signature: bytes, key_id: str) -> VerifyResponse:
    """Verify a signature using AWS KMS."""
    client = get_kms_client()

    try:
        # Hash the message
        message_digest = hashlib.sha256(message.encode("utf-8")).digest()

        response = client.verify(
            KeyId=key_id,
            Message=message_digest,
            MessageType="DIGEST",
            Signature=signature,
            SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA_256",
        )

        is_valid = response["SignatureValid"]

        return VerifyResponse(
            success=True,
            is_valid=is_valid,
            key_id=key_id,
            algorithm="RSASSA_PKCS1_V1_5_SHA_256",
            provider="aws_kms",
        )
    except Exception as e:
        return VerifyResponse(success=False, error=str(e), provider="aws_kms")
