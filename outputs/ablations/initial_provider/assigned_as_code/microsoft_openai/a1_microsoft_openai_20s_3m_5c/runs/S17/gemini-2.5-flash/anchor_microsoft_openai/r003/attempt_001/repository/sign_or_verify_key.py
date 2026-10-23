from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient, SignatureAlgorithm

def sign_or_verify_key(data, config=None, operation='sign'):
    config = config or {}
    with DefaultAzureCredential() as credential:
        key_id = config.get('key_id')
        if not key_id:
            raise ValueError("Key ID is required for signing or verification.")

        with CryptographyClient(key_id, credential=credential) as client:
            if operation == 'sign':
                # Hash the data before signing if the key expects a hash
                import hashlib
                digest = hashlib.sha256(data['payload']).digest()
                sign_response = client.sign(SignatureAlgorithm.rs256, digest)
                return {'signature': sign_response.signature, 'key_id': sign_response.key_id, 'algorithm': 'RS256'}
            elif operation == 'verify':
                import hashlib
                digest = hashlib.sha256(data['payload']).digest()
                verify_response = client.verify(SignatureAlgorithm.rs256, digest, data['signature'])
                return {'is_valid': verify_response.is_valid, 'key_id': key_id, 'algorithm': 'RS256'}
            else:
                raise ValueError("Operation must be 'sign' or 'verify'.")
