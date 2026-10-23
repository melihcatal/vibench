from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient, SignatureAlgorithm

from security_models import normalize_signature_payload


def sign_or_verify_key(payload, config=None):
    config = config or {}
    normalized = normalize_signature_payload(payload)
    with DefaultAzureCredential() as credential:
        with CryptographyClient(normalized.get('key_id') or config['key_id'], credential=credential) as client:
            if normalized.get('verify_only'):
                return {'verified': client.verify(SignatureAlgorithm.rs256, normalized['data'], normalized['signature']).is_valid}
            signature = client.sign(SignatureAlgorithm.rs256, normalized['data'])
    return {'signature': signature.signature, 'key_id': signature.key_id, 'algorithm': 'RS256'}
