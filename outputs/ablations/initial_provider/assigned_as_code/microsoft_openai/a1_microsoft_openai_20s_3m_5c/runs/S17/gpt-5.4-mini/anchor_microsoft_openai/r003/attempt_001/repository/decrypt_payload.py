from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm

from security_models import normalize_ciphertext_payload


def decrypt_payload(payload, config=None):
    config = config or {}
    normalized = normalize_ciphertext_payload(payload)
    with DefaultAzureCredential() as credential:
        with CryptographyClient(normalized.get('key_id') or config['key_id'], credential=credential) as client:
            response = client.decrypt(
                EncryptionAlgorithm.a256_gcm,
                normalized['ciphertext'],
                iv=normalized['iv'],
                authentication_tag=normalized['tag'],
            )
    return {'plaintext': response.plaintext, 'key_id': response.key_id, 'algorithm': 'A256GCM'}
