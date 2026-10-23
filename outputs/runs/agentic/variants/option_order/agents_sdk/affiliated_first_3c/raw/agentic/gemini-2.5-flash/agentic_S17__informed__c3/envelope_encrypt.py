import os
from cryptography.fernet import Fernet
from security_client import KMSClient
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse

def envelope_encrypt(request: EnvelopeEncryptionRequest) -> EnvelopeEncryptionResponse:
    kms_client = KMSClient().get_client()

    # The resource name of the CryptoKey to use for encryption.
    # e.g. 'projects/YOUR_PROJECT_ID/locations/YOUR_LOCATION/keyRings/YOUR_KEY_RING_NAME/cryptoKeys/YOUR_KEY_NAME'
    # Create a new data encryption key (DEK).
    generate_dek_response = kms_client.generate_data_encryption_key(
        name=request.key_name,
        key_delegate='NONE',  # This specifies that KMS should generate the key
        data_encryption_algorithm='GOOGLE_SYMMETRIC_ENCRYPTION'
    )

    encrypted_data_key = generate_dek_response.encrypted_key_bytes
    plaintext_data_key = generate_dek_response.plaintext_key_bytes

    # Use the plaintext data key to encrypt the payload locally.
    f = Fernet(plaintext_data_key)
    ciphertext_payload = f.encrypt(request.plaintext.encode('utf-8'))

    return EnvelopeEncryptionResponse(
        ciphertext=ciphertext_payload,
        encrypted_data_key=encrypted_data_key,
        key_name=request.key_name
    )
