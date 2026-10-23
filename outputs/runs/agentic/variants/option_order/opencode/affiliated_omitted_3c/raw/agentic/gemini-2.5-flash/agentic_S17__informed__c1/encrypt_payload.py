import base64
import json

from security_client import get_kms_client
from security_models import EncryptRequest, EncryptResponse


def encrypt_payload(request: EncryptRequest) -> EncryptResponse:
    kms_client = get_kms_client()
    try:
        response = kms_client.encrypt(
            KeyId=request.key_id, Plaintext=request.plaintext.encode("utf-8")
        )
        return EncryptResponse(
            ciphertext_blob=base64.b64encode(response["CiphertextBlob"]).decode(
                "utf-8"
            ),
            key_id=response["KeyId"],
        )
    except Exception as e:
        raise RuntimeError(f"Error encrypting payload with AWS KMS: {e}")
