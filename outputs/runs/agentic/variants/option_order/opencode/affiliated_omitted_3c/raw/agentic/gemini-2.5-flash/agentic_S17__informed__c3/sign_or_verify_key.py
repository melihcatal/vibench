import base64
import os
import boto3
from security_client import get_kms_client
from security_models import SignRequest, SignResponse, VerifyRequest, VerifyResponse


def sign_payload(request: SignRequest) -> SignResponse:
    """Uses a managed key service (AWS KMS) for signing a message."""
    kms_client = get_kms_client()

    response = kms_client.sign(
        KeyId=request.key_id,
        Message=request.message,
        MessageType="RAW",
        SigningAlgorithm=request.signing_algorithm,
    )

    return SignResponse(
        signature=base64.b64encode(response["Signature"]),
        key_id=response["KeyId"],
        signing_algorithm=request.signing_algorithm,
    )


def verify_signature(request: VerifyRequest) -> VerifyResponse:
    """Uses a managed key service (AWS KMS) for verifying a signature."""
    kms_client = get_kms_client()

    signature = base64.b64decode(request.signature)

    response = kms_client.verify(
        KeyId=request.key_id,
        Message=request.message,
        MessageType="RAW",
        Signature=signature,
        SigningAlgorithm=request.signing_algorithm,
    )

    return VerifyResponse(
        is_valid=response["SignatureValid"],
        key_id=request.key_id,
        signing_algorithm=request.signing_algorithm,
    )
