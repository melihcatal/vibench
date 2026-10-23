import base64
from cryptography.fernet import Fernet
from security_client import get_kms_client
from security_models import (
    EnvelopeEncryptionRequest, 
    EnvelopeEncryptionResponse,
    EnvelopeDecryptionRequest,
    DecryptionResponse
)

def envelope_encrypt(request: EnvelopeEncryptionRequest) -> EnvelopeEncryptionResponse:
    """
    Performs envelope encryption.
    1. Generates a data key from AWS KMS.
    2. Uses the plaintext key to encrypt data locally.
    3. Returns the encrypted data and the encrypted data key.
    """
    kms_client = get_kms_client()
    
    data_key_response = kms_client.generate_data_key(
        KeyId=request.key_id,
        KeySpec='AES_256'
    )
    
    plaintext_data_key = data_key_response['Plaintext']
    encrypted_data_key = data_key_response['CiphertextBlob']
    
    fernet_key = base64.urlsafe_b64encode(plaintext_data_key)
    f = Fernet(fernet_key)
    
    ciphertext = f.encrypt(request.plaintext)
    
    return EnvelopeEncryptionResponse(
        encrypted_data_key=encrypted_data_key,
        ciphertext=ciphertext
    )

def envelope_decrypt(request: EnvelopeDecryptionRequest) -> DecryptionResponse:
    """
    Performs envelope decryption.
    1. Decrypts the encrypted data key using AWS KMS.
    2. Uses the plaintext data key to decrypt the data locally.
    """
    kms_client = get_kms_client()

    decrypted_key_response = kms_client.decrypt(
        CiphertextBlob=request.encrypted_data_key
    )
    plaintext_data_key = decrypted_key_response['Plaintext']
    
    fernet_key = base64.urlsafe_b64encode(plaintext_data_key)
    f = Fernet(fernet_key)

    plaintext = f.decrypt(request.ciphertext)

    return DecryptionResponse(
        plaintext=plaintext,
        key_id=decrypted_key_response['KeyId']
    )
