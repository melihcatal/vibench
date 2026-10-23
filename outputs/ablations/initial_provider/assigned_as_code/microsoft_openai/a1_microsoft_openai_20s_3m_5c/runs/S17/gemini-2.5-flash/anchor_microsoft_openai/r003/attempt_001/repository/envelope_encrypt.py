from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient, KeyWrapAlgorithm

def envelope_encrypt(payload, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        key_id = config.get('key_id')
        if not key_id:
            raise ValueError("Key ID is required for envelope encryption.")

        with CryptographyClient(key_id, credential=credential) as client:
            # Generate a symmetric content encryption key (CEK) locally
            import os
            content_encryption_key = os.urandom(32)  # 256-bit key for AES256

            # Wrap the CEK with the Azure Key Vault key
            wrap_response = client.wrap_key(KeyWrapAlgorithm.rsa_oaep, content_encryption_key)

            # Encrypt the payload with the locally generated CEK (e.g., using AES GCM)
            # For this example, we'll use a placeholder for actual payload encryption
            # In a real scenario, you would use a library like cryptography to encrypt
            # the payload with content_encryption_key and a randomly generated IV/tag.
            encrypted_payload_data = b"encrypted_data_placeholder"
            iv = os.urandom(16) # Placeholder IV
            tag = os.urandom(16) # Placeholder tag

    return {
        'wrapped_content_encryption_key': wrap_response.encrypted_key,
        'key_id': wrap_response.key_id,
        'encrypted_payload_data': encrypted_payload_data,
        'iv': iv,
        'tag': tag,
        'algorithm': 'RSA-OAEP_and_AES256GCM_Placeholder'
    }
