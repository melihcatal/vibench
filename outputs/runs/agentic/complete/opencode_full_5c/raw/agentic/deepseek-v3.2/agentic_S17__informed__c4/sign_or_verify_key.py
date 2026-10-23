import os
import base64
import hashlib
from security_client import get_kms_client
from security_models import SignRequest, VerifyRequest, SignResponse, VerifyResponse


def sign_data(data: str, key_id: str) -> SignResponse:
    """
    Sign data using AWS KMS asymmetric signing.
    """
    client = get_kms_client()

    try:
        # Hash the data first
        message_digest = hashlib.sha256(data.encode("utf-8")).digest()

        response = client.sign(
            KeyId=key_id,
            Message=message_digest,
            MessageType="DIGEST",
            SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA_256",
        )

        signature_b64 = base64.b64encode(response["Signature"]).decode("utf-8")

        return SignResponse(
            success=True,
            signature=signature_b64,
            key_id=key_id,
            algorithm="RSASSA_PKCS1_V1_5_SHA_256",
            provider="aws_kms",
        )
    except Exception as e:
        return SignResponse(success=False, error=str(e), provider="aws_kms")


def verify_signature(data: str, signature_b64: str, key_id: str) -> VerifyResponse:
    """
    Verify a signature using AWS KMS.
    """
    client = get_kms_client()

    try:
        # Hash the data
        message_digest = hashlib.sha256(data.encode("utf-8")).digest()

        signature = base64.b64decode(signature_b64)

        response = client.verify(
            KeyId=key_id,
            Message=message_digest,
            MessageType="DIGEST",
            Signature=signature,
            SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA_256",
        )

        return VerifyResponse(
            success=True,
            valid=response["SignatureValid"],
            key_id=key_id,
            algorithm="RSASSA_PKCS1_V1_5_SHA_256",
            provider="aws_kms",
        )
    except Exception as e:
        return VerifyResponse(success=False, error=str(e), provider="aws_kms")
