from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm

def envelope_encrypt(plaintext, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with CryptographyClient(config['key_id'], credential=credential) as client:
            response = client.encrypt(EncryptionAlgorithm.a256_gcm, plaintext)
            data_encryption_key = response.ciphertext
            response = client.encrypt(EncryptionAlgorithm.a256_gcm, data_encryption_key)
            return {'ciphertext': response.ciphertext, 'iv': response.iv, 'tag': response.authentication_tag,
                    'key_id': response.key_id, 'algorithm': 'A256GCM'}