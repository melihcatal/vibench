from security_client import get_kms_client
from security_models import to_bytes, b64encode
from cryptography.fernet import Fernet

def envelope_encrypt(plaintext: str, key_id: str) -> dict[str, str]:
    plaintext_bytes = to_bytes(plaintext)
    dek = Fernet.generate_key()
    fernet = Fernet(dek)
    local_ciphertext = fernet.encrypt(plaintext_bytes)
    client = get_kms_client()
    kms_response = client.encrypt(KeyId=key_id, Plaintext=dek)
    encrypted_dek = b64encode(kms_response['CiphertextBlob'])
    local_ct_b64 = b64encode(local_ciphertext)
    return {
        'encrypted_dek': encrypted_dek,
        'ciphertext': local_ct_b64
    }