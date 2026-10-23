from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm

def decrypt_payload(ciphertext, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with CryptographyClient(config['key_id'], credential=credential) as client:
            response = client.decrypt(EncryptionAlgorithm.a256_gcm, ciphertext['ciphertext'], ciphertext['iv'], ciphertext['tag'])
    return {'plaintext': response.plaintext, 'key_id': response.key_id, 'algorithm': 'A256GCM'}