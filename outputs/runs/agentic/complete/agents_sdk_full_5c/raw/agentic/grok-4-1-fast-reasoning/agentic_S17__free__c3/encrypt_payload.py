from security_client import kms_client, SYMMETRIC_KEY_ID
from security_models import b64encode, normalize_payload

def encrypt_payload(payload: str) -> str:
    plaintext = normalize_payload(payload)
    response = kms_client.encrypt(
        KeyId=SYMMETRIC_KEY_ID,
        Plaintext=plaintext
    )
    return b64encode(response['CiphertextBlob'])
