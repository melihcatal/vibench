import base64
from security_client import SecurityClient
from security_models import SignRequest, SignResponse, VerifyRequest, VerifyResponse

def sign_payload(request: SignRequest) -> SignResponse:
    kms_client = SecurityClient().get_kms_client()
    response = kms_client.sign(
        KeyId=request.key_id,
        Message=request.message,
        MessageType='RAW',
        SigningAlgorithm=request.signing_algorithm
    )
    return SignResponse(
        signature=base64.b64encode(response['Signature']),
        key_id=response['KeyId'] if 'KeyId' in response else request.key_id,
        signing_algorithm=response['SigningAlgorithm'] if 'SigningAlgorithm' in response else request.signing_algorithm
    )

def verify_signature(request: VerifyRequest) -> VerifyResponse:
    kms_client = SecurityClient().get_kms_client()
    response = kms_client.verify(
        KeyId=request.key_id,
        Message=request.message,
        MessageType='RAW',
        Signature=base64.b64decode(request.signature),
        SigningAlgorithm=request.signing_algorithm
    )
    return VerifyResponse(
        signature_valid=response['SignatureValid'],
        key_id=request.key_id
    )
