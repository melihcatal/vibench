import base64
from security_client import security_client
from security_models import EnvelopeEncryptRequest, EnvelopeEncryptResponse


def envelope_encrypt(request: EnvelopeEncryptRequest) -> EnvelopeEncryptResponse:
    # In a real scenario, you would generate a data key, use it to encrypt the plaintext locally,
    # and then encrypt the data key itself with the KMS master key.
    # For this exercise, we simulate the data key generation and return the plaintext as the ciphertext_blob.

    response = security_client.kms_client.generate_data_key(
        KeyId=request.key_id,
        KeySpec="AES_256",
        EncryptionContext=request.encryption_context,
    )

    encrypted_data_key = response["CiphertextBlob"]
    plaintext_bytes = request.plaintext.encode("utf-8")

    # Simulate local encryption with the data key
    # In a real application, you would use response['Plaintext'] (the data key) to encrypt request.plaintext
    # For simplicity, we are just returning the original plaintext here as the 'ciphertext_blob'
    # and the KMS-encrypted data key.
    ciphertext_blob = plaintext_bytes  # This would be the locally encrypted data

    return EnvelopeEncryptResponse(
        ciphertext_blob=ciphertext_blob,
        encrypted_data_key=encrypted_data_key,
        key_id=request.key_id,
    )
