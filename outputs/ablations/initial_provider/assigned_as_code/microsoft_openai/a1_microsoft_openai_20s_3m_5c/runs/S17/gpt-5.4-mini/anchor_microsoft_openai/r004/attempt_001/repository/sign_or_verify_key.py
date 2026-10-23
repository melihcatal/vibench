from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient, SignatureAlgorithm


def sign_or_verify_key(payload, config=None):
    config = config or {}
    action = payload.get('action', 'sign')
    with DefaultAzureCredential() as credential:
        with CryptographyClient(config['key_id'], credential=credential) as client:
            if action == 'verify':
                result = client.verify(SignatureAlgorithm.es256, payload['digest'], payload['signature'])
                return {'valid': result.is_valid, 'key_id': result.key_id, 'algorithm': 'ES256'}
            response = client.sign(SignatureAlgorithm.es256, payload['digest'])
            return {'signature': response.signature, 'key_id': response.key_id, 'algorithm': 'ES256'}
