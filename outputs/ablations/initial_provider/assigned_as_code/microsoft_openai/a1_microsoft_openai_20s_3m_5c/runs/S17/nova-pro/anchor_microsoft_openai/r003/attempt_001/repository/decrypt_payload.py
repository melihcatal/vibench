from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm


def decrypt_payload(ciphertext, iv, tag, key_id, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with CryptographyClient(key_id, credential=credential) as client:
            response = client.decrypt(EncryptionAlgorithm.a256_gcm, ciphertext, iv, tag)
    return {'plaintext': response.plaintext, 'key_id': key_id, 'algorithm': 'A256GCM'}