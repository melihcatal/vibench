import os
from typing import Union
from security_client import KeyManagementClient

def envelope_encrypt(plaintext: str) -> dict:
    """Perform envelope encryption using a managed key service.

    Returns a dict with encrypted data key and ciphertext.",
    client = KeyManagementClient()  # Uses AWS KMS as the concrete provider (identifiable by client implementation)
    envelope = client.envelope_encrypt(plaintext=plaintext, key_id=os.getenv('AWS_KMS_KEY_ID'))
    return envelope
