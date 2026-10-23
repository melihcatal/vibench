from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient


def sign_or_verify_key(payload, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with CryptographyClient(config['key_id'], credential=credential) as client:
            if payload['action'] == 'sign':
                signature = client.sign(payload['algorithm'], payload['data'])
                return {'signature': signature.signature, 'key_id': signature.key_id, 'algorithm': payload['algorithm']}
            elif payload['action'] == 'verify':
                verification = client.verify(payload['algorithm'], payload['data'], payload['signature'])
                return {'is_valid': verification.is_valid, 'key_id': verification.key_id, 'algorithm': payload['algorithm']}