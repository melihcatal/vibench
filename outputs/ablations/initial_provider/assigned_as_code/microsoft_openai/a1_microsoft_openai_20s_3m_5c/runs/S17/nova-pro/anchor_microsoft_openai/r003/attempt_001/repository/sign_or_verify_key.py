from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient, SignatureAlgorithm


def sign_or_verify_key(data, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with CryptographyClient(config['key_id'], credential=credential) as client:
            if config.get('sign'):
                signature = client.sign(SignatureAlgorithm.rsassa_pss, data)
                return {'signature': signature.signature, 'key_id': signature.key_id, 'algorithm': 'RSassaPSS'}
            elif config.get('verify'):
                client.verify(SignatureAlgorithm.rsassa_pss, data, config['signature'])
                return {'verified': True, 'key_id': config['key_id'], 'algorithm': 'RSassaPSS'}
            else:
                raise ValueError('Must specify either sign or verify')
