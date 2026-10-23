from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient

def sign_or_verify_key(payload, key_id, action):
    credential = DefaultAzureCredential()
    with CryptographyClient(key_id, credential=credential) as client:
        if action == 'sign':
            response = client.sign(algorithm='ES256', digest=payload)
            return response.signature
        elif action == 'verify':
            response = client.verify(algorithm='ES256', digest=payload, signature=key_id)
            return response.is_valid
        else:
            raise ValueError('Invalid action. Use either sign or verify.')