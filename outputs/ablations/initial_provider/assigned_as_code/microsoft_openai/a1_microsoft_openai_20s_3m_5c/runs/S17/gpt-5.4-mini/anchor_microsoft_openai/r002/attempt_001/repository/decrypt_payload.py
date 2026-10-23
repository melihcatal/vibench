from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm

from security_client import load_security_config, normalize_key_id


def decrypt_payload(payload, config=None):
    config = load_security_config(config)
    key_id = normalize_key_id(config) or config['key_id']
    with DefaultAzureCredential() as credential:
        with CryptographyClient(key_id, credential=credential) as client:
            response = client.decrypt(
                EncryptionAlgorithm.a256_gcm,
                payload['ciphertext'],
                iv=payload['iv'],
                authentication_tag=payload['tag'],
            )
    return {'plaintext': response.plaintext, 'key_id': response.key_id, 'algorithm': 'A256GCM'}
