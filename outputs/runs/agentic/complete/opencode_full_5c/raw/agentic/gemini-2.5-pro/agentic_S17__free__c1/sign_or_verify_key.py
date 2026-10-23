from security_client import get_kms_client
from security_models import (
    SigningRequest,
    SigningResponse,
    VerificationRequest,
    VerificationResponse,
)


def sign_message(request: SigningRequest) -> SigningResponse:
    kms_client = get_kms_client()

    response = kms_client.sign(
        KeyId=request.key_id,
        Message=request.message,
        MessageType="RAW",
        SigningAlgorithm=request.signing_algorithm,
    )

    return SigningResponse(
        key_id=response["KeyId"],
        signature=response["Signature"],
        algorithm=response["SigningAlgorithm"],
    )


def verify_signature(request: VerificationRequest) -> VerificationResponse:
    kms_client = get_kms_client()

    try:
        response = kms_client.verify(
            KeyId=request.key_id,
            Message=request.message,
            MessageType="RAW",
            Signature=request.signature,
            SigningAlgorithm=request.signing_algorithm,
        )
        is_valid = response["SignatureValid"]
    except kms_client.exceptions.KMSInvalidSignatureException:
        is_valid = False
        response = {"SigningAlgorithm": request.signing_algorithm}

    return VerificationResponse(
        key_id=request.key_id, is_valid=is_valid, algorithm=response["SigningAlgorithm"]
    )
