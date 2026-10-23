import base64
from cryptography.fernet import Fernet
from security_client import SecurityClient, get_kms_key_id
from security_models import EnvelopeEncryptionResult

def envelope_encrypt(plaintext: bytes) -> EnvelopeEncryptionResult:
    """
    Implements envelope encryption using AWS KMS to generate a data key.
    """
    kms_client = SecurityClient.get_kms_client()
    key_id = get_kms_key_id()

    # 1. Generate a data key from KMS
    # This returns a plaintext key and an encrypted version of it
    response = kms_client.generate_data_key(
        KeyId=key_id,
        KeySpec='AES_256'
    )

    plaintext_data_key = response['Plaintext']
    encrypted_data_key = response['CiphertextBlob']

    # 2. Use the plaintext data key to encrypt the data locally
    # Fernet keys must be 32 url-safe base64-encoded bytes.
    fernet_key = base64.urlsafe_b64encode(plaintext_data_key)
    f = Fernet(fernet_key)
    encrypted_data = f.encrypt(plaintext)

    # 3. Discard the plaintext data key
    del plaintext_data_key

    # 4. Return the encrypted data and the encrypted data key
    return EnvelopeEncryptionResult(
        encrypted_data=encrypted_data,
        encrypted_data_key=encrypted_data_key
    )
