import os
import json
from security_client import KmsClient
from security_models import EncryptRequest, EncryptResponse

# Use AWS KMS as the concrete managed key service
# The client loads AWS credentials from environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

def encrypt_payload(plaintext: str, key_id: str) -> str:
    """Encrypts plaintext using AWS KMS and returns the ciphertext (base64 encoded).

    The function builds an EncryptRequest, sends it to AWS KMS via the KmsClient,
    and returns a JSON string representing the EncryptResponse.
    """
    client = KmsClient()
    request = EncryptRequest(KeyId=key_id, Plaintext=plaintext)
    # Call the AWS KMS API via boto3 (handled internally by KmsClient)
    response = client.encrypt(request)
    # Normalize the response to our local model
    normalized = EncryptResponse(**response)
    return json.dumps(normalized.dict())

if __name__ == "__main__":
    # Example usage (remove or protect real keys in production)
    pt = "Hello, world!"
    key = "alias/MyKMSEncryptionKey"
    print("Ciphertext:", encrypt_payload(pt, key))