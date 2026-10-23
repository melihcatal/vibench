from security_client import get_cryptography_client
from azure.keyvault.keys.crypto import SignatureAlgorithm
import os


def sign_payload(payload_data, key_name=None):
    key_id = os.environ.get("SIGNING_KEY_ID")
    if not key_id:
        raise ValueError("SIGNING_KEY_ID environment variable not set.")

    client = get_cryptography_client(key_id)
    # Azure Key Vault expects bytes for signing
    if isinstance(payload_data, str):
        payload_data = payload_data.encode('utf-8')

    # Use PS256 for signing with RSA key
    sign_result = client.sign(SignatureAlgorithm.ps256, payload_data)
    return {'signature': sign_result.signature, 'key_id': key_id, 'algorithm': 'PS256'}


def verify_signature(payload_data, signature, key_id):
    client = get_cryptography_client(key_id)
    if isinstance(payload_data, str):
        payload_data = payload_data.encode('utf-8')

    verify_result = client.verify(SignatureAlgorithm.ps256, payload_data, signature)
    return {'is_valid': verify_result.is_valid, 'key_id': key_id}
