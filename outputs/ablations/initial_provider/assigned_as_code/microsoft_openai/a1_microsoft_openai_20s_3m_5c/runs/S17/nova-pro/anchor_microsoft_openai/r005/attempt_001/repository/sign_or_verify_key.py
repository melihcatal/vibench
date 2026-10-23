from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient

def sign_or_verify_key(message, signature, key_id):
    config = {}
    config['key_id'] = key_id
    with DefaultAzureCredential() as credential:
        with CryptographyClient(config['key_id'], credential=credential) as client:
            response = client.verify_data(signature, message)
    return response.is_valid
