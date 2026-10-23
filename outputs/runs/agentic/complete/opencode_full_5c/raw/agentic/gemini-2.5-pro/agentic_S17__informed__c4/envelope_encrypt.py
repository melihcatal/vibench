from cryptography.fernet import Fernet
from security_client import get_kms_client
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse


def envelope_encrypt(request: EnvelopeEncryptionRequest) -> EnvelopeEncryptionResponse:
    """
    Implements envelope encryption using AWS KMS to generate a data key.
    """
    kms_client = get_kms_client()

    # Generate a data key from KMS
    data_key_response = kms_client.generate_data_key(
        KeyId=request.key_id, KeySpec="AES_256"
    )

    plaintext_data_key = data_key_response["Plaintext"]
    encrypted_data_key = data_key_response["CiphertextBlob"]

    # Use the plaintext data key to encrypt the payload locally
    f = Fernet(plaintext_data_key)
    ciphertext = f.encrypt(request.plaintext)

    return EnvelopeEncryptionResponse(
        ciphertext=ciphertext, encrypted_data_key=encrypted_data_key
    )
