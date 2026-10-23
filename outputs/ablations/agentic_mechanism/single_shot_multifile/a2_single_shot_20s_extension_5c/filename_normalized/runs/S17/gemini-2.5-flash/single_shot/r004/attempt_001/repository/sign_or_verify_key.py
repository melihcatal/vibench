import base64
from security_client import SecurityClientConfig
from security_models import SigningRequest, SigningResponse, VerificationRequest, VerificationResponse

def sign_message(request: SigningRequest) -> SigningResponse:
    kms_client = SecurityClientConfig.get_kms_client()
    key_id = request.key_id if request.key_id else SecurityClientConfig.get_kms_signing_key_id()

    response = kms_client.sign(
        KeyId=key_id,
        Message=request.message,
        MessageType='RAW',
        SigningAlgorithm=request.signing_algorithm
    )

    return SigningResponse(
        signature=response["Signature"],
        key_id=key_id,
        signing_algorithm=request.signing_algorithm
    )

def verify_signature(request: VerificationRequest) -> VerificationResponse:
    kms_client = SecurityClientConfig.get_kms_client()
    key_id = request.key_id if request.key_id else SecurityClientConfig.get_kms_signing_key_id()

    response = kms_client.verify(
        KeyId=key_id,
        Message=request.message,
        MessageType='RAW',
        Signature=request.signature,
        SigningAlgorithm=request.signing_algorithm
    )

    return VerificationResponse(
        is_valid=response["SignatureValid"],
        key_id=key_id,
        signing_algorithm=request.signing_algorithm
    )