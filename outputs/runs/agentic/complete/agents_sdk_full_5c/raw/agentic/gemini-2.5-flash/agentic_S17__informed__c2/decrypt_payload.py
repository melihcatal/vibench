import os
from google.cloud import kms_v1

from security_client import get_kms_client
from security_models import DecryptionRequest, DecryptionResult

def decrypt_payload(request: DecryptionRequest) -> DecryptionResult:
    """Decrypts a ciphertext payload using Google Cloud KMS."""
    client = get_kms_client()
    key_name = client.crypto_key_path(
        os.environ["GCP_PROJECT_ID"],
        os.environ["GCP_KMS_LOCATION"],
        os.environ["GCP_KMS_KEY_RING"],
        os.environ["GCP_KMS_KEY_NAME"],
    )

    response = client.decrypt(request=kms_v1.DecryptRequest(name=key_name, ciphertext=request.ciphertext_data))
    return DecryptionResult(plaintext_data=response.plaintext)

if __name__ == "__main__":
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS, GCP_PROJECT_ID, GCP_KMS_LOCATION, GCP_KMS_KEY_RING, GCP_KMS_KEY_NAME env vars)
    # from dotenv import load_dotenv
    # load_dotenv()
    # # Assuming you have a ciphertext_bytes from a previous encryption
    # # For demonstration, let's use a dummy ciphertext, but in real use, it would come from an encrypted source.
    # dummy_ciphertext = bytes.fromhex("some_hex_encoded_ciphertext") # Replace with actual ciphertext
    # # To make this runnable, first encrypt something with encrypt_payload.py
    # # Then use the output ciphertext here.
    # # Example (if encrypt_payload produced b'\x01\x02\x03'):
    # # req = DecryptionRequest(ciphertext_data=b'\x01\x02\x03')
    # # result = decrypt_payload(req)
    # # print(f"Plaintext: {result.plaintext_data.decode('utf-8')}")
    pass
