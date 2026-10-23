import boto3
from security_client import SecurityClient
from security_models import SigningRequest, SigningResponse, VerificationRequest, VerificationResponse


def sign_message(request: SigningRequest, config=None) -> SigningResponse:
    config = config or {}
    client = SecurityClient(region_name=config.get("region"))
    response = client.sign(
        key_id=request.key_id,
        message=request.message,
        signing_algorithm=request.signing_algorithm,
        message_type=request.message_type
    )
    return SigningResponse(
        signature=response["Signature"],
        key_id=response["KeyId"],
        signing_algorithm=request.signing_algorithm
    )


def verify_signature(request: VerificationRequest, config=None) -> VerificationResponse:
    config = config or {}
    client = SecurityClient(region_name=config.get("region"))
    response = client.verify(
        key_id=request.key_id,
        message=request.message,
        signature=request.signature,
        signing_algorithm=request.signing_algorithm,
        message_type=request.message_type
    )
    return VerificationResponse(
        signature_valid=response["SignatureValid"],
        key_id=request.key_id,
        signing_algorithm=request.signing_algorithm
    )
