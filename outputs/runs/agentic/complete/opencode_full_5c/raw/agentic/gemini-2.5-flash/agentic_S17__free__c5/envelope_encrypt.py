import os
from google.cloud import kms_v1
from google.cloud.kms_v1 import types
from cryptography.fernet import Fernet
import base64


def envelope_encrypt(
    project_id: str, location_id: str, key_ring_id: str, key_id: str, plaintext: bytes
) -> tuple[bytes, bytes]:
    """
    Implements envelope encryption using Google Cloud KMS for the data encryption key (DEK)
    and Fernet for local encryption.
    Returns the encrypted payload and the wrapped DEK.
    """
    kms_client = kms_v1.KeyManagementServiceClient()
    key_name = kms_client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # 1. Generate a new data encryption key (DEK) using KMS
    generate_dek_request = types.GenerateSymmetricBytesRequest(
        name=key_name,
        generate_unwrapped=True,  # Request unwrapped DEK for local encryption
        include_plaintext_key_alt_uri=False,  # Don't include plaintext in response
    )
    dek_response = kms_client.generate_symmetric_bytes(request=generate_dek_request)
    wrapped_dek = dek_response.ciphertext  # This is the DEK encrypted by KMS
    unwrapped_dek = (
        dek_response.plaintext
    )  # This is the plaintext DEK for local encryption

    # 2. Use the unwrapped DEK to encrypt the payload locally
    # Fernet keys must be URL-safe base64-encoded.
    fernet_key = base64.urlsafe_b64encode(unwrapped_dek)
    f = Fernet(fernet_key)
    encrypted_payload = f.encrypt(plaintext)

    return encrypted_payload, wrapped_dek


if __name__ == "__main__":
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    LOCATION_ID = os.environ.get("GOOGLE_CLOUD_KMS_LOCATION", "global")
    KEY_RING_ID = os.environ.get("GOOGLE_CLOUD_KMS_KEY_RING", "my-key-ring")
    KEY_ID = os.environ.get("GOOGLE_CLOUD_KMS_KEY_ID", "my-envelope-kek")

    sample_plaintext = b"This is a very secret message for envelope encryption."
    encrypted_data, wrapped_dek = envelope_encrypt(
        PROJECT_ID, LOCATION_ID, KEY_RING_ID, KEY_ID, sample_plaintext
    )

    print(f"Envelope Encrypted Payload: {encrypted_data.hex()}")
    print(f"Wrapped Data Encryption Key (DEK): {wrapped_dek.hex()}")
