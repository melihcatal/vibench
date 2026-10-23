from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm

from security_client import load_security_config, normalize_key_id


def envelope_encrypt(payload, config=None):
    config = load_security_config(config)
    key_id = normalize_key_id(config) or config['key_id']
    with DefaultAzureCredential() as credential:
        with CryptographyClient(key_id, credential=credential) as client:
            key_wrap = client.wrap_key(EncryptionAlgorithm.rsa_oaep, payload['data_key'])
    return {
        'wrapped_key': key_wrap.encrypted_key,
        'key_id': key_wrap.key_id,
        'algorithm': 'RSA-OAEP',
        'encrypted_payload': payload.get('encrypted_payload'),
        'iv': payload.get('iv'),
        'tag': payload.get('tag'),
    }
