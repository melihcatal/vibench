import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient


def load_security_config(config=None):
    data = dict(config or {})
    if 'key_id' not in data:
        data['key_id'] = os.getenv('AZURE_KEY_VAULT_KEY_ID', '')
    if 'vault_url' not in data:
        data['vault_url'] = os.getenv('AZURE_KEY_VAULT_URL', '')
    return data


def get_credential():
    return DefaultAzureCredential()


def get_crypto_client(key_id, credential=None):
    credential = credential or get_credential()
    return CryptographyClient(key_id, credential=credential)


def normalize_bytes(value):
    if value is None:
        return b''
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode('utf-8')
    return bytes(value)


def normalize_result(response):
    result = {'key_id': getattr(response, 'key_id', None)}
    for field in ('ciphertext', 'plaintext', 'iv', 'authentication_tag', 'signature'):
        if hasattr(response, field):
            result[field] = getattr(response, field)
    return result
