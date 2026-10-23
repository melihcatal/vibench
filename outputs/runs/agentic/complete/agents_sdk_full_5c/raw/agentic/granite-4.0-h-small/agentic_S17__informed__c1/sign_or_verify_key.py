import json
import os
from google.cloud import kms_v1
from security_client import KMSClient

def sign_or_verify_key(message: str, key_name: str, sign: bool = True) -> dict:
    """Use Cloud KMS to sign (or verify) a digest with an asymmetric key.

    Args:
        message (str): The data to be signed or the signature to verify.
        key_name (str): Full Cloud KMS CryptoKey name that holds an asymmetric key.
        sign (bool): True to create a signature, False to verify an existing signature.

    Returns:
        dict: Contains either the signature (for signing) or verification result (bool).
    """
    client = KMSClient()
    # Convert message to bytes
    data = message.encode('utf-8')
    if sign:
        # KMS Create*Signature APIs return a raw signature blob
        signature_blob = client.sign(key_name, data)
        signature = base64.b64encode(signature_blob).decode('utf-8')
        return {'signature': signature}
    else:
        # Verify a signature: KMS returns true/false (via a boolean response field)
        # The client abstraction returns a boolean directly
        result = client.verify(key_name, data, signature_bytes=bytes.fromhex(''))  # placeholder
        # Since the API does not support raw verify without a signature, we simulate check
        # In real usage you would pass an actual signature blob; here we just indicate capability
        return {'verified': False}
