import os
from cryptography.fernet import Fernet
from botocore.exceptions import ClientError
from security_client import kms_client
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse

def envelope_encrypt_payload(request: EnvelopeEncryptionRequest) -> EnvelopeEncryptionResponse:
    """
    Performs envelope encryption.
    1. Generate a data key from AWS KMS.
    2. Use the plaintext data key to encrypt the payload locally.
    3. Return the encrypted payload and the encrypted data key.
    """
    try:
        kms = kms_client.get_client()

        # 1. Generate data key
        data_key_response = kms.generate_data_key(
            KeyId=request.key_id,
            KeySpec='AES_256'
        )
        plaintext_key = data_key_response['Plaintext']
        encrypted_data_key = data_key_response['CiphertextBlob']

        # 2. Encrypt payload locally
        f = Fernet(base64.urlsafe_b64encode(plaintext_key))
        encrypted_payload = f.encrypt(request.plaintext)

        return EnvelopeEncryptionResponse(
            ciphertext=encrypted_payload,
            encrypted_data_key=encrypted_data_key,
            success=True
        )
    except ClientError as e:
        return EnvelopeEncryptionResponse(
            ciphertext=b'',
            encrypted_data_key=b'',
            success=False,
            error=str(e)
        )
