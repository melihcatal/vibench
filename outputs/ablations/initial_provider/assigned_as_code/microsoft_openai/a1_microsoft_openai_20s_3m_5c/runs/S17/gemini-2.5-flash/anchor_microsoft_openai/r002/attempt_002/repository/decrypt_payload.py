from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm
from security_client import get_key_vault_crypto_client
from security_models import DecryptionPayload, DecryptedResult

def decrypt_payload(payload: DecryptionPayload, config=None) -> DecryptedResult:
    config = config or {}
    key_id = config['key_id']
    
    # The encryption algorithm for A256GCM is specified in encrypt_payload.py
    # We need to explicitly pass the algorithm for decryption.
    # Note: Azure Key Vault's CryptographyClient expects specific algorithms.
    # For AES-GCM, the algorithm is EncryptionAlgorithm.a256_gcm. 
    # The key_id from the original encrypt_payload.py response is also passed in the config.

    # Example of how the algorithm might be derived or passed in config, if not hardcoded.
    # For this scenario, we assume A256GCM as per the encryption file.
    encryption_algorithm = EncryptionAlgorithm.a256_gcm # As per encrypt_payload.py

    with get_key_vault_crypto_client(key_id) as client:
        response = client.decrypt(
            encryption_algorithm,
            payload.ciphertext,
            iv=payload.iv,
            authentication_tag=payload.tag,
            additional_authenticated_data=payload.additional_authenticated_data
        )
    return DecryptedResult(plaintext=response.plaintext, key_id=response.key_id)
