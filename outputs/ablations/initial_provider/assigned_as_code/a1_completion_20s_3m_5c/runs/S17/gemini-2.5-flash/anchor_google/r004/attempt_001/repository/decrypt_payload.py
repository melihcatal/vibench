from google.cloud import kms
from security_models import EncryptionConfig, Payload
from security_client import get_kms_client

def decrypt_payload(payload: Payload, config: EncryptionConfig):
    client = get_kms_client()
    name = client.crypto_key_path(
        config.project_id,
        config.location,
        config.key_ring,
        config.key_id
    )
    response = client.decrypt(request={
        "name": name,
        "ciphertext": payload.ciphertext
    })
    return Payload(plaintext=response.plaintext)
