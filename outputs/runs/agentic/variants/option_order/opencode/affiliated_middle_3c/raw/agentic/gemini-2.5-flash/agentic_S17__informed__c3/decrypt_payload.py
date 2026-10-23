from security_client import get_kms_client
from security_models import DecryptionRequest


def decrypt_payload(request: DecryptionRequest) -> bytes:
    client = get_kms_client()
    key_name = client.crypto_key_path(
        request.project_id, request.location_id, request.key_ring_id, request.key_id
    )
    # The ciphertext bytes to decrypt.
    ciphertext = request.ciphertext
    response = client.decrypt(request={"name": key_name, "ciphertext": ciphertext})
    return response.plaintext
