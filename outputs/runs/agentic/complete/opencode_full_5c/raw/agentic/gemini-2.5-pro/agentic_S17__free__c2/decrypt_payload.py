from security_client import get_aws_kms_client
from security_models import DecryptionPayload


def decrypt_data(payload: DecryptionPayload) -> bytes:
    kms_client = get_aws_kms_client()
    response = kms_client.decrypt(CiphertextBlob=payload.ciphertext)
    return response["Plaintext"]
