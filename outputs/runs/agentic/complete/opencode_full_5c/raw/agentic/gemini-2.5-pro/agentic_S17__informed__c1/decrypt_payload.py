from security_client import get_kms_client
from security_models import DecryptionPayload
import base64


def decrypt(payload: DecryptionPayload) -> bytes:
    kms_client = get_kms_client()

    decoded_ciphertext = base64.b64decode(payload.ciphertext)

    response = kms_client.decrypt(
        KeyId=payload.key_id, CiphertextBlob=decoded_ciphertext
    )
    return response["Plaintext"]
