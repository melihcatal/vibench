from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm


def encrypt_payload(payload, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with CryptographyClient(config['key_id'], credential=credential) as client:
            response = client.encrypt(EncryptionAlgorithm.a256_gcm, payload['plaintext'])
    # AES-GCM needs the IV and authentication tag as well as ciphertext for decryption.
    return {'ciphertext': response.ciphertext, 'iv': response.iv, 'tag': response.authentication_tag,
            'key_id': response.key_id, 'algorithm': 'A256GCM'}
