from security_client import get_kms_client
from security_models import EncryptionRequest


def encrypt_payload(request: EncryptionRequest) -> bytes:
    client = get_kms_client()
    key_name = client.crypto_key_path(
        request.project_id, request.location_id, request.key_ring_id, request.key_id
    )
    # The plaintext bytes to encrypt. This can be a bytes object or a bytearray.
    plaintext = request.plaintext
    response = client.encrypt(request={"name": key_name, "plaintext": plaintext})
    return response.ciphertext
