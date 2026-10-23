from security_client import get_security_client
from security_models import (
    SigningRequest,
    SigningResponse,
    VerificationRequest,
    VerificationResponse,
)


def sign_payload(request: SigningRequest) -> SigningResponse:
    kms_client = get_security_client()

    response = kms_client.sign(
        KeyId=request.key_id,
        Message=request.message,
        MessageType="RAW",
        SigningAlgorithm=request.signing_algorithm,
    )

    return SigningResponse(
        key_id=request.key_id,
        signature=response["Signature"],
        signing_algorithm=response["SigningAlgorithm"],
    )


def verify_signature(request: VerificationRequest) -> VerificationResponse:
    kms_client = get_security_client()

    try:
        response = kms_client.verify(
            KeyId=request.key_id,
            Message=request.message,
            MessageType="RAW",
            Signature=request.signature,
            SigningAlgorithm=request.signing_algorithm,
        )
        is_valid = response.get("SignatureValid", False)
    except kms_client.exceptions.KMSInvalidSignatureException:
        is_valid = False

    return VerificationResponse(key_id=request.key_id, is_valid=is_valid)
