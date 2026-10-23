from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm

def decrypt_payload(ciphertext, iv, tag, key_id):
    config = {}
    config['key_id'] = key_id
    with DefaultAzureCredential() as credential:
        with CryptographyClient(config['key_id'], credential=credential) as client:
            response = client.decrypt(EncryptionAlgorithm.a256_gcm, ciphertext, iv, tag)
    return response.plaintext
