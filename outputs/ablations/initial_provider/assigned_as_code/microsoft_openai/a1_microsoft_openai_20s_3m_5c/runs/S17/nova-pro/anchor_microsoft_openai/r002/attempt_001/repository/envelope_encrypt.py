from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient


def envelope_encrypt(payload, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with CryptographyClient(config['key_id'], credential=credential) as client:
            data_key = client.encrypt(EncryptionAlgorithm.a256_gcm, b'')
            encrypted_payload = client.encrypt(EncryptionAlgorithm.a256_gcm, payload['plaintext'], iv=data_key.iv)
    return {'ciphertext': encrypted_payload.ciphertext, 'iv': encrypted_payload.iv, 'tag': encrypted_payload.authentication_tag,
            'key_id': data_key.key_id, 'algorithm': 'A256GCM', 'data_key_ciphertext': data_key.ciphertext, 'data_key_iv': data_key.iv, 'data_key_tag': data_key.authentication_tag}