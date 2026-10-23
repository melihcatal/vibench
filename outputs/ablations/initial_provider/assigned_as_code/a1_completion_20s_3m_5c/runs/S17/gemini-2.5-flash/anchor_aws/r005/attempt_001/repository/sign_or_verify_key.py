from security_client import SecurityClient
from security_models import SigningResponse, VerificationResponse

def sign_payload(message: bytes, key_id: str, region: str, signing_algorithm: str) -> SigningResponse:
    security_client = SecurityClient(region_name=region)
    response = SigningResponse()
    try:
        signature = security_client.sign(
            key_id=key_id,
            message=message,
            signing_algorithm=signing_algorithm
        )
        response.signature = signature
        response.signing_algorithm = signing_algorithm
    except Exception as e:
        response.error = str(e)
    return response

def verify_signature(message: bytes, signature: bytes, key_id: str, region: str, signing_algorithm: str) -> VerificationResponse:
    security_client = SecurityClient(region_name=region)
    response = VerificationResponse()
    try:
        is_valid = security_client.verify(
            key_id=key_id,
            message=message,
            signature=signature,
            signing_algorithm=signing_algorithm
        )
        response.signature_valid = is_valid
    except Exception as e:
        response.error = str(e)
    return response
