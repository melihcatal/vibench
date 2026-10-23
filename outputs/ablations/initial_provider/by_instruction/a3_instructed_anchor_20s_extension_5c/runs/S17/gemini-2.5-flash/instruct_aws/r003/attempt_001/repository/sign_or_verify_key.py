from security_client import get_kms_client
from security_models import SignatureRequest, SignatureResponse, VerificationRequest, VerificationResponse

def sign_message(request: SignatureRequest) -> SignatureResponse:
    """
    Signs a message using an asymmetric key in AWS KMS.
    """
    kms_client = get_kms_client()
    response = kms_client.sign(
        KeyId=request.key_id,
        Message=request.message.encode('utf-8'),
        MessageType=request.message_type,
        SigningAlgorithm=request.signing_algorithm
    )
    return SignatureResponse(
        signature=response['Signature'],
        key_id=request.key_id,
        signing_algorithm=request.signing_algorithm
    )

def verify_signature(request: VerificationRequest) -> VerificationResponse:
    """
    Verifies a signature using an asymmetric key in AWS KMS.
    """
    kms_client = get_kms_client()
    response = kms_client.verify(
        KeyId=request.key_id,
        Message=request.message.encode('utf-8'),
        MessageType=request.message_type,
        Signature=request.signature,
        SigningAlgorithm=request.signing_algorithm
    )
    return VerificationResponse(
        signature_valid=response['SignatureValid'],
        key_id=request.key_id,
        signing_algorithm=request.signing_algorithm
    )
