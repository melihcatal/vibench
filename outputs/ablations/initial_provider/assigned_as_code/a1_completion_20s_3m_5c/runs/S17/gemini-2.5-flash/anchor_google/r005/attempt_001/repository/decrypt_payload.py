from google.cloud import kms
from security_models import DecryptionConfig
from security_client import get_kms_client

def decrypt_payload(payload: dict, config: DecryptionConfig):
    client = get_kms_client()
    name = client.crypto_key_path(
        config.project_id, config.location, config.key_ring, config.key_id
    )
    response = client.decrypt(request={
        "name": name,
        "ciphertext": payload["ciphertext"]
    })
    return {"plaintext": response.plaintext}
