from security_client import get_kms_client
from security_models import SignRequest, SignResponse, VerifyRequest, VerifyResponse


def sign_message(request: SignRequest) -> SignResponse:
    """
    Uses AWS KMS to sign a message.
    """
    kms_client = get_kms_client()
    response = kms_client.sign(
        KeyId=request.key_id,
        Message=request.message,
        MessageType="RAW",
        SigningAlgorithm=request.signing_algorithm,
    )
    return SignResponse(signature=response["Signature"], key_id=response["KeyId"])


def verify_signature(request: VerifyRequest) -> VerifyResponse:
    """
    Uses AWS KMS to verify a signature.
    """
    kms_client = get_kms_client()
    try:
        response = kms_client.verify(
            KeyId=request.key_id,
            Message=request.message,
            MessageType="RAW",
            Signature=request.signature,
            SigningAlgorithm=request.signing_algorithm,
        )
        return VerifyResponse(
            signature_valid=response["SignatureValid"], key_id=response["KeyId"]
        )
    except kms_client.exceptions.KMSInvalidSignatureException:
        return VerifyResponse(signature_valid=False, key_id=request.key_id)
