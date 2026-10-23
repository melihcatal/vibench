import os
import json
from security_client import SecurityClient
from security_models import DecryptionRequest, normalize_payload, serialize_response


def decrypt_payload(ciphertext: str, context: dict = None) -> str:
    client = SecurityClient()
    request = DecryptionRequest(ciphertext=ciphertext, context=context)
    normalized = normalize_payload(request.dict())

    plaintext = client.decrypt_symmetric(normalized["ciphertext"])

    response = {
        "plaintext": plaintext.decode(),
        "key_id": os.getenv("GOOGLE_KMS_KEY_NAME"),
        "algorithm": "GOOGLE_SYMMETRIC_ENCRYPTION",
    }
    return serialize_response(response)
