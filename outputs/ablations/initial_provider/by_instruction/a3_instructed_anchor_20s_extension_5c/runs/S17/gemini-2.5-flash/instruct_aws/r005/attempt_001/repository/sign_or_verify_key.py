import base64
from security_client import SecurityClient

class SigningRequest:
    def __init__(self, message: str, key_id: str, signing_algorithm: str):
        self.message = message
        self.key_id = key_id
        self.signing_algorithm = signing_algorithm

class SigningResponse:
    def __init__(self, signature: bytes, key_id: str, signing_algorithm: str):
        self.signature = base64.b64encode(signature).decode('utf-8')
        self.key_id = key_id
        self.signing_algorithm = signing_algorithm

class VerificationRequest:
    def __init__(self, message: str, signature: str, key_id: str, signing_algorithm: str):
        self.message = message
        self.signature = signature
        self.key_id = key_id
        self.signing_algorithm = signing_algorithm

class VerificationResponse:
    def __init__(self, signature_valid: bool):
        self.signature_valid = signature_valid

def sign_message(request: SigningRequest) -> SigningResponse:
    client = SecurityClient()
    kms_client = client.get_kms_client()

    sign_response = kms_client.sign(
        KeyId=request.key_id,
        Message=request.message.encode('utf-8'),
        MessageType='RAW',
        SigningAlgorithm=request.signing_algorithm
    )

    return SigningResponse(
        signature=sign_response['Signature'],
        key_id=sign_response['KeyId'],
        signing_algorithm=request.signing_algorithm
    )

def verify_signature(request: VerificationRequest) -> VerificationResponse:
    client = SecurityClient()
    kms_client = client.get_kms_client()

    signature_bytes = base64.b64decode(request.signature)

    verify_response = kms_client.verify(
        KeyId=request.key_id,
        Message=request.message.encode('utf-8'),
        MessageType='RAW',
        Signature=signature_bytes,
        SigningAlgorithm=request.signing_algorithm
    )

    return VerificationResponse(
        signature_valid=verify_response['SignatureValid']
    )