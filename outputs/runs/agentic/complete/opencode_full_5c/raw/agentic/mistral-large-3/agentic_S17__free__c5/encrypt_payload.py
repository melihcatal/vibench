import os
import json
from security_client import SecurityClient
from security_models import EncryptionRequest, normalize_payload, serialize_response


def encrypt_payload(plaintext: str, context: dict = None) -> str:
    client = SecurityClient()
    request = EncryptionRequest(plaintext=plaintext, context=context)
    normalized = normalize_payload(request.dict())

    ciphertext = client.encrypt_symmetric(normalized["plaintext"])

    response = {
        "ciphertext": ciphertext,
        "key_id": os.getenv("GOOGLE_KMS_KEY_NAME"),
        "algorithm": "GOOGLE_SYMMETRIC_ENCRYPTION",
    }
    return serialize_response(response)
