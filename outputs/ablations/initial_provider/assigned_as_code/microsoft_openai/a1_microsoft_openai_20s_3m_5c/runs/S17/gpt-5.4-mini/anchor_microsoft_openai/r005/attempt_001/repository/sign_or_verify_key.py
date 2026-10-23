from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient, SignatureAlgorithm

from security_models import normalize_bytes


def sign_or_verify_key(payload, config=None):
    config = config or {}
    message = normalize_bytes(payload['message'])
    with DefaultAzureCredential() as credential:
        with CryptographyClient(config['key_id'], credential=credential) as client:
            if payload.get('operation') == 'verify':
                return {
                    'verified': client.verify(SignatureAlgorithm.rs256, message, normalize_bytes(payload['signature'])).is_valid,
                    'key_id': config['key_id'],
                    'algorithm': 'RS256',
                }
            response = client.sign(SignatureAlgorithm.rs256, message)
    return {'signature': response.signature, 'key_id': response.key_id, 'algorithm': 'RS256'}
