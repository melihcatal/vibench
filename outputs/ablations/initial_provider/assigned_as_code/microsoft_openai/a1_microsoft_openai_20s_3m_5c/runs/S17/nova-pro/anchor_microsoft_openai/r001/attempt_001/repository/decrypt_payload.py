from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient

def decrypt_payload(ciphertext, iv, tag, key_id):
    credential = DefaultAzureCredential()
    with CryptographyClient(key_id, credential=credential) as client:
        response = client.decrypt(algorithm='A256GCM', ciphertext=ciphertext, iv=iv, tag=tag)
    return response.plaintext