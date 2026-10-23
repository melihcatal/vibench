from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient, SignatureAlgorithm

from security_client import load_security_config, normalize_key_id


def sign_or_verify_key(payload, config=None):
    config = load_security_config(config)
    key_id = normalize_key_id(config) or config['key_id']
    with DefaultAzureCredential() as credential:
        with CryptographyClient(key_id, credential=credential) as client:
            if payload.get('mode') == 'verify':
                verified = client.verify(
                    SignatureAlgorithm.rs256,
                    payload['digest'],
                    payload['signature'],
                )
                return {'verified': verified.verified, 'key_id': key_id, 'algorithm': 'RS256'}
            signed = client.sign(SignatureAlgorithm.rs256, payload['digest'])
            return {'signature': signed.signature, 'key_id': signed.key_id, 'algorithm': 'RS256'}
