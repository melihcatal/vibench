from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient

def envelope_encrypt(plaintext, key_id):
    credential = DefaultAzureCredential()
    with CryptographyClient(key_id, credential=credential) as client:
        response = client.encrypt(algorithm='A256GCM', plaintext=plaintext)
    return {'ciphertext': response.ciphertext, 'iv': response.iv, 'tag': response.authentication_tag, 'key_id': response.key_id, 'algorithm': 'A256GCM'}