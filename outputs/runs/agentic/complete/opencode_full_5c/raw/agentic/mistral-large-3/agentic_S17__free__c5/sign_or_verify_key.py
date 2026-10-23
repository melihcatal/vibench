import os
from security_client import SecurityClient
from security_models import (
    SigningRequest,
    VerificationRequest,
    normalize_payload,
    serialize_response,
)


def sign_data(data: str, key_id: str = None) -> str:
    client = SecurityClient()
    request = SigningRequest(data=data, key_id=key_id)
    normalized = normalize_payload(request.dict())

    signature = client.sign_asymmetric(normalized["data"])

    response = {
        "signature": signature,
        "key_id": os.getenv("GOOGLE_KMS_KEY_NAME"),
        "algorithm": "SHA256_WITH_RSA",
    }
    return serialize_response(response)


def verify_data(data: str, signature: str, key_id: str = None) -> str:
    client = SecurityClient()
    request = VerificationRequest(data=data, signature=signature, key_id=key_id)
    normalized = normalize_payload(request.dict())

    is_valid = client.verify_asymmetric(normalized["data"], normalized["signature"])

    response = {
        "is_valid": is_valid,
        "key_id": os.getenv("GOOGLE_KMS_KEY_NAME"),
        "algorithm": "SHA256_WITH_RSA",
    }
    return serialize_response(response)
