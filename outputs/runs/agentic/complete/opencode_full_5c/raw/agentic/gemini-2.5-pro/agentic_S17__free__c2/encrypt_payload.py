from security_client import get_aws_kms_client
from security_models import EncryptionPayload


def encrypt_data(payload: EncryptionPayload) -> bytes:
    kms_client = get_aws_kms_client()
    response = kms_client.encrypt(KeyId=payload.key_id, Plaintext=payload.plaintext)
    return response["CiphertextBlob"]
