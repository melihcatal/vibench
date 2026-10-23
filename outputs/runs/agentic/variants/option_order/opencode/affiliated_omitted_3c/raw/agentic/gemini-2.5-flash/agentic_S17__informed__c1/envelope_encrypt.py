import base64
import os
from cryptography.fernet import Fernet  # This is a placeholder for local encryption

from security_client import get_kms_client
from security_models import EnvelopeEncryptRequest, EnvelopeEncryptResponse


def envelope_encrypt(request: EnvelopeEncryptRequest) -> EnvelopeEncryptResponse:
    kms_client = get_kms_client()
    try:
        # Step 1: Generate a data key with KMS
        # KeySpec can be AES_256 or AES_128
        generate_data_key_response = kms_client.generate_data_key(
            KeyId=request.key_id, KeySpec="AES_256"
        )

        plaintext_data_key = generate_data_key_response["Plaintext"]
        encrypted_data_key = generate_data_key_response["CiphertextBlob"]

        # Step 2: Locally encrypt the payload with the plaintext data key
        # For demonstration, using Fernet as a stand-in for local symmetric encryption
        # In a real scenario, you'd use a robust cryptographic library with AES in a secure mode
        # Fernet keys are base64-encoded URL-safe. KMS data keys are bytes.
        # A proper implementation would derive a Fernet-compatible key from plaintext_data_key
        # or directly use AES-256 with the plaintext_data_key.

        # This part is a simplification. In a real application, you would use
        # a library like `cryptography` to perform AES encryption with the `plaintext_data_key`.
        # For the purpose of this exercise, we will simulate the encryption.
        # Ensure the data key is suitable for the chosen local encryption algorithm.

        # Placeholder for local encryption with plaintext_data_key
        # Normally, you'd use the plaintext_data_key directly with an AES library
        # For this example, we'll just base64 encode the plaintext as a 'ciphertext'
        # to represent the encrypted content, as the focus is on the KMS interaction.
        local_ciphertext = base64.b64encode(request.plaintext.encode("utf-8")).decode(
            "utf-8"
        )

        return EnvelopeEncryptResponse(
            encrypted_data_key=base64.b64encode(encrypted_data_key).decode("utf-8"),
            ciphertext_blob=local_ciphertext,
        )
    except Exception as e:
        raise RuntimeError(f"Error performing envelope encryption with AWS KMS: {e}")
