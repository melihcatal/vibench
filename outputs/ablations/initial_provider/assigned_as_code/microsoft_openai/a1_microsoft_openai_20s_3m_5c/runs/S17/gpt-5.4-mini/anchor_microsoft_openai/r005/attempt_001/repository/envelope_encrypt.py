from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm
from azure.storage.blob import BlobServiceClient

from security_models import normalize_bytes


def envelope_encrypt(payload, config=None):
    config = config or {}
    plaintext = normalize_bytes(payload['plaintext'])
    with DefaultAzureCredential() as credential:
        with CryptographyClient(config['key_id'], credential=credential) as client:
            data_key = client.wrap_key("RSA-OAEP", payload['data_key'])
            ciphertext = client.encrypt(EncryptionAlgorithm.a256_gcm, plaintext)
    blob_client = BlobServiceClient(account_url=config['blob_account_url'], credential=credential).get_blob_client(
        container=config['container'], blob=config['blob_name']
    )
    blob_client.upload_blob(data_key.encrypted_key, overwrite=True)
    return {
        'ciphertext': ciphertext.ciphertext,
        'iv': ciphertext.iv,
        'tag': ciphertext.authentication_tag,
        'wrapped_key': data_key.encrypted_key,
        'key_id': ciphertext.key_id,
        'algorithm': 'A256GCM',
    }
