from security_client import get_kms_client
from security_models import EncryptionRequest
from dataclasses import dataclass
from cryptography.fernet import Fernet

@dataclass
class EnvelopeEncryptionResponse:
    encrypted_data_key: bytes
    encrypted_payload: bytes
    key_id: str

def envelope_encrypt(request: EncryptionRequest) -> EnvelopeEncryptionResponse:
    """
    Implements envelope encryption using AWS KMS to generate a data key
    and Fernet for local payload encryption.
    """
    kms_client = get_kms_client()
    
    # Generate a data key from KMS
    generate_data_key_response = kms_client.generate_data_key(
        KeyId=request.key_id,
        KeySpec='AES_256'
    )
    
    plaintext_data_key = generate_data_key_response['Plaintext']
    encrypted_data_key = generate_data_key_response['CiphertextBlob']
    
    # Use the plaintext data key to encrypt the payload locally with Fernet
    # Fernet key must be URL-safe base64-encoded
    f = Fernet(plaintext_data_key)
    encrypted_payload = f.encrypt(request.plaintext.encode('utf-8'))
    
    # Clean up plaintext data key from memory
    del plaintext_data_key

    return EnvelopeEncryptionResponse(
        encrypted_data_key=encrypted_data_key,
        encrypted_payload=encrypted_payload,
        key_id=request.key_id
    )
