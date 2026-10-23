from cryptography.fernet import Fernet
import base64
from security_client import kms_client, SYMMETRIC_KEY_ID
from security_models import b64encode, normalize_payload, EnvelopeCiphertext

def envelope_encrypt(payload: str) -> EnvelopeCiphertext:
    plaintext = normalize_payload(payload)
    generate_response = kms_client.generate_data_key(
        KeyId=SYMMETRIC_KEY_ID,
        KeySpec='AES_256'
    )
    plaintext_key = generate_response['Plaintext']
    encrypted_key = generate_response['CiphertextBlob']
    fernet_key = base64.urlsafe_b64encode(plaintext_key)
    f = Fernet(fernet_key)
    ciphertext = f.encrypt(plaintext)
    return EnvelopeCiphertext(
        encrypted_key=b64encode(encrypted_key),
        ciphertext=b64encode(ciphertext)
    )
