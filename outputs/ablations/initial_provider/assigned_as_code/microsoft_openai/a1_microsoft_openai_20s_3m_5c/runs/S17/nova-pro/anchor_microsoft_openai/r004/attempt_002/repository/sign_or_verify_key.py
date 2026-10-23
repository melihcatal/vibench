from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient, SignatureAlgorithm

def sign_or_verify_key(payload, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with CryptographyClient(config['key_id'], credential=credential) as client:
            response = client.sign(SignatureAlgorithm.rsassa_pss, payload)
            return {'signature': response.signature, 'key_id': response.key_id, 'algorithm': 'RS256'}