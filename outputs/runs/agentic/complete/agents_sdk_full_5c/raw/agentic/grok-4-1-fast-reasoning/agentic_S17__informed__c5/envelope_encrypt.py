import base64
from cryptography.fernet import Fernet
from typing import Dict, Any
from security_client import get_kms_client
from security_models import KeyConfig, normalize_payload, BytesOrStr

def envelope_encrypt(plaintext: BytesOrStr, key_id: str, region: str = 'us-east-1') -> Dict[str, bytes]:
    client = get_kms_client(KeyConfig(key_id=key_id, region=region))
    plaintext_bytes = normalize_payload(plaintext)
    
    data_key_resp = client.generate_data_key(
        KeyId=key_id,
        KeySpec='AES_256'
    )
    dek = data_key_resp['Plaintext']
    encrypted_dek = data_key_resp['CiphertextBlob']
    
    fernet_key = base64.urlsafe_b64encode(dek)
    f = Fernet(fernet_key)
    ciphertext = f.encrypt(plaintext_bytes)
    
    return {
        'ciphertext': ciphertext,
        'encrypted_dek': encrypted_dek
    }
