from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm
from azure.keyvault.keys import KeyVaultKey

def decrypt_payload(payload, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        # The key ID is typically retrieved from the encryption response or configuration
        key_id = payload.get('key_id') or config.get('key_id')
        if not key_id:
            raise ValueError("Key ID is required for decryption.")

        # Reconstruct the KeyVaultKey object if only the ID is available
        # or directly use the key_id string to initialize the client if it's a full key identifier
        
        # The CryptographyClient expects the key_id to be the full identifier of the key,
        # not just the key_vault_name.
        # Assuming payload['key_id'] or config['key_id'] is the full key identifier.
        with CryptographyClient(key_id, credential=credential) as client:
            response = client.decrypt(
                EncryptionAlgorithm.a256_gcm,
                payload['ciphertext'],
                iv=payload['iv'],
                authentication_tag=payload['tag']
            )
    return {'plaintext': response.plaintext}
