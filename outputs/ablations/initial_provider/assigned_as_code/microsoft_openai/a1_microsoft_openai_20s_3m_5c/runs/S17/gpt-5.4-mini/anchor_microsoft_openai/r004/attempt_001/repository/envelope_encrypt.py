from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm


def envelope_encrypt(payload, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with CryptographyClient(config['key_id'], credential=credential) as client:
            response = client.wrap_key(EncryptionAlgorithm.rsa_oaep, payload['data_key'])
    return {'encrypted_key': response.encrypted_key, 'key_id': response.key_id, 'algorithm': 'RSA-OAEP', 'nonce': payload.get('nonce'), 'ciphertext': payload.get('ciphertext')}
