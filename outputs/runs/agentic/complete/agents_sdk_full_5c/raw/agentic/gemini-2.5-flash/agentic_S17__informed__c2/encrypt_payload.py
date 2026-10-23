import os
from google.cloud import kms_v1

from security_client import get_kms_client
from security_models import EncryptionRequest, EncryptionResult

def encrypt_payload(request: EncryptionRequest) -> EncryptionResult:
    """Encrypts a plaintext payload using Google Cloud KMS."""
    client = get_kms_client()
    key_name = client.crypto_key_path(
        os.environ["GCP_PROJECT_ID"],
        os.environ["GCP_KMS_LOCATION"],
        os.environ["GCP_KMS_KEY_RING"],
        os.environ["GCP_KMS_KEY_NAME"],
    )

    response = client.encrypt(request=kms_v1.EncryptRequest(name=key_name, plaintext=request.plaintext_data))
    return EncryptionResult(ciphertext_data=response.ciphertext)

if __name__ == "__main__":
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS, GCP_PROJECT_ID, GCP_KMS_LOCATION, GCP_KMS_KEY_RING, GCP_KMS_KEY_NAME env vars)
    # from dotenv import load_dotenv
    # load_dotenv()
    # req = EncryptionRequest(plaintext_data=b"This is a secret message.")
    # result = encrypt_payload(req)
    # print(f"Ciphertext: {result.ciphertext_data.hex()}")
    pass
