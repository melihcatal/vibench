from security_client import get_kms_client
from security_models import SigningRequest, SigningResponse, VerificationRequest, VerificationResponse

def sign_with_kms(request: SigningRequest) -> SigningResponse:
    """
    Signs a message using an asymmetric key in AWS KMS.
    """
    kms_client = get_kms_client()

    response = kms_client.sign(
        KeyId=request.key_id,
        Message=request.message,
        MessageType='RAW',
        SigningAlgorithm=request.signing_algorithm
    )

    return SigningResponse(
        signature=response['Signature'],
        key_id=response['KeyId'],
        signing_algorithm=response['SigningAlgorithm']
    )

def verify_with_kms(request: VerificationRequest) -> VerificationResponse:
    """
    Verifies a signature using an asymmetric key in AWS KMS.
    """
    kms_client = get_kms_client()

    try:
        response = kms_client.verify(
            KeyId=request.key_id,
            Message=request.message,
            MessageType='RAW',
            Signature=request.signature,
            SigningAlgorithm=request.signing_algorithm
        )
        return VerificationResponse(is_valid=response['SignatureValid'])
    except kms_client.exceptions.KMSInvalidSignatureException:
        return VerificationResponse(is_valid=False)
