import base64
import json

from security_client import get_kms_client
from security_models import DecryptRequest, DecryptResponse


def decrypt_payload(request: DecryptRequest) -> DecryptResponse:
    kms_client = get_kms_client()
    try:
        response = kms_client.decrypt(
            CiphertextBlob=base64.b64decode(request.ciphertext_blob)
        )
        return DecryptResponse(
            plaintext=response["Plaintext"].decode("utf-8"), key_id=response["KeyId"]
        )
    except Exception as e:
        raise RuntimeError(f"Error decrypting payload with AWS KMS: {e}")
