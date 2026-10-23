import os
import json
from security_client import KmsClient
from security_models import DecryptRequest, DecryptResponse

# Use AWS KMS as the concrete managed key service
# The client loads AWS credentials from environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

def decrypt_payload(ciphertext_b64: str, key_id: str) -> str:
    """Decrypts ciphertext (base64‑encoded) using AWS KMS and returns the plaintext string.

    Builds a DecryptRequest, sends it via KmsClient, and normalizes the response.
    """
    client = KmsClient()
    request = DecryptRequest(CiphertextBlob=ciphertext_b64)
    response = client.decrypt(request)
    normalized = DecryptResponse(**response)
    return normalized.Plaintext.decode('utf-8')

if __name__ == "__main__":
    # Example usage (requires a ciphertext previously encrypted with the same key_id)
    ct_b64 = "YOUR_BASE64_CIPHERTEXT"
    key_id = "alias/MyKMSEncryptionKey"
    print("Plaintext:", decrypt_payload(ct_b64, key_id))
