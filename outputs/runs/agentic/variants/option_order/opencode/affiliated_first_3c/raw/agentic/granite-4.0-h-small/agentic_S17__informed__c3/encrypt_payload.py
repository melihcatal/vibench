import os
from typing import Dict, Any
from security_client import KeyManagementClient

def encrypt_payload(plaintext: str) -> Dict[str, Any]:
    """Encrypt a plaintext payload using a managed key.

    Returns a dictionary containing ciphertext and metadata from the Key Management and Encryption service.",
    client = KeyManagementClient()  # Uses AWS KMS as the concrete provider (identifiable by client implementation)
    response = client.encrypt(plaintext=plaintext, key_id=os.getenv('AWS_KMS_KEY_ID'))
    return response
