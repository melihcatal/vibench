from security_client import get_kms_client
from security_models import to_bytes, serialize_blob
import base64
from cryptography.fernet import Fernet

def envelope_encrypt(plaintext: str, key_id: str) -> tuple[str, str]:
    client = get_kms_client()
    response = client.generate_data_key(
        KeyId=key_id,
        KeySpec='AES_256'
    )
    plaintext_key = response['Plaintext']
    encrypted_key = response['CiphertextBlob']
    
    fernet_key = base64.urlsafe_b64encode(plaintext_key)
    f = Fernet(fernet_key)
    encrypted_data = f.encrypt(to_bytes(plaintext))
    
    return serialize_blob(encrypted_data), serialize_blob(encrypted_key)