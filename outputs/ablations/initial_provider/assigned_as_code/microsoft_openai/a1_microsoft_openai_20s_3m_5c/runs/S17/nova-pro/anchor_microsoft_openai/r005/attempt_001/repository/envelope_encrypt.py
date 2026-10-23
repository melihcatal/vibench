from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm

def envelope_encrypt(plaintext, key_id):
    config = {}
    config['key_id'] = key_id
    with DefaultAzureCredential() as credential:
        with CryptographyClient(config['key_id'], credential=credential) as client:
            response = client.encrypt(EncryptionAlgorithm.a256_gcm, plaintext)
    encrypted_data_key = client.encrypt(config['key_id'], response.ciphertext)
    return encrypted_data_key.ciphertext, response.ciphertext, response.iv, response.authentication_tag
