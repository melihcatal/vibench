from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm
from azure.keyvault.keys import KeyClient


def envelope_encrypt(plaintext, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        key_client = KeyClient(config['key_vault_url'], credential)
        key = key_client.get_key(config['key_name'])
        data_encryption_key = os.urandom(32)  # Generate a random data encryption key
        data_encryption_client = CryptographyClient(key.id, credential)
        encrypted_data_key = data_encryption_client.encrypt(EncryptionAlgorithm.rsa_oaep, data_encryption_key)
        data_encryption_client = CryptographyClient(config['key_id'], credential)
        encrypted_data = data_encryption_client.encrypt(EncryptionAlgorithm.a256_gcm, plaintext, data_encryption_key)
    return {'encrypted_data_key': encrypted_data_key.ciphertext, 'encrypted_data': encrypted_data.ciphertext, 'iv': encrypted_data.iv, 'tag': encrypted_data.authentication_tag, 'key_id': encrypted_data.key_id, 'algorithm': 'A256GCM'}