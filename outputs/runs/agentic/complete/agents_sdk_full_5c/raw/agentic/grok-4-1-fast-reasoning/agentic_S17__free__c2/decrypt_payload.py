from security_client import get_kms_client
from security_models import deserialize_blob, bytes_to_str

def decrypt_payload(ciphertext: str, key_id: str = None) -> str:
    client = get_kms_client()
    response = client.decrypt(CiphertextBlob=deserialize_blob(ciphertext))
    return bytes_to_str(response['Plaintext'])