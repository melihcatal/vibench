from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm


def decrypt_payload(payload, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with CryptographyClient(config['key_id'], credential=credential) as client:
            response = client.decrypt(EncryptionAlgorithm.a256_gcm, payload['ciphertext'], iv=payload['iv'], authentication_tag=payload['tag'])
    return {'plaintext': response.plaintext, 'key_id': response.key_id, 'algorithm': 'A256GCM'}
