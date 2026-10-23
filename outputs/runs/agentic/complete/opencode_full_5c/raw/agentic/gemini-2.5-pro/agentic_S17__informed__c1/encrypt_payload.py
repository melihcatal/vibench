from security_client import get_kms_client
from security_models import EncryptionPayload
import base64


def encrypt(payload: EncryptionPayload) -> str:
    kms_client = get_kms_client()
    response = kms_client.encrypt(KeyId=payload.key_id, Plaintext=payload.plaintext)
    return base64.b64encode(response["CiphertextBlob"]).decode("utf-8")
