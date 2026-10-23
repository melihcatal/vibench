from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm

from security_models import normalize_bytes


def decrypt_payload(payload, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with CryptographyClient(config['key_id'], credential=credential) as client:
            response = client.decrypt(
                EncryptionAlgorithm.a256_gcm,
                normalize_bytes(payload['ciphertext']),
                iv=normalize_bytes(payload.get('iv')),
                authentication_tag=normalize_bytes(payload.get('tag')),
            )
    return {'plaintext': response.plaintext, 'key_id': response.key_id, 'algorithm': 'A256GCM'}
