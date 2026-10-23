from security_client import get_cryptography_client
from azure.keyvault.keys.crypto import EncryptionAlgorithm
import os
from cryptography.fernet import Fernet


def envelope_encrypt(plaintext_payload, key_name=None):
    key_id = os.environ.get("KEY_ID_FOR_ENVELOPE") # Master key in Key Vault
    if not key_id:
        raise ValueError("KEY_ID_FOR_ENVELOPE environment variable not set for master key.")

    # Step 1: Generate a data encryption key (DEK) locally
    data_key = Fernet.generate_key()
    f = Fernet(data_key)
    
    # Step 2: Encrypt the plaintext payload with the local DEK
    encrypted_payload = f.encrypt(plaintext_payload.encode('utf-8'))

    # Step 3: Encrypt the DEK with the master key in Azure Key Vault
    cryptography_client = get_cryptography_client(key_id)
    encrypted_data_key_response = cryptography_client.encrypt(EncryptionAlgorithm.rsa_oaep, data_key)

    return {
        'encrypted_payload': encrypted_payload,
        'encrypted_data_key': encrypted_data_key_response.ciphertext,
        'key_id': key_id, # The ID of the master key in Key Vault
        'encrypted_data_key_algorithm': 'RSA-OAEP'
    }

def envelope_decrypt(encrypted_envelope_payload):
    key_id = encrypted_envelope_payload.get('key_id')
    encrypted_data_key = encrypted_envelope_payload.get('encrypted_data_key')
    encrypted_payload = encrypted_envelope_payload.get('encrypted_payload')

    if not all([key_id, encrypted_data_key, encrypted_payload]):
        raise ValueError("Missing components for envelope decryption.")
    
    # Step 1: Decrypt the DEK with the master key in Azure Key Vault
    cryptography_client = get_cryptography_client(key_id)
    decrypted_data_key_response = cryptography_client.decrypt(EncryptionAlgorithm.rsa_oaep, encrypted_data_key)
    data_key = decrypted_data_key_response.plaintext

    # Step 2: Decrypt the payload with the local DEK
    f = Fernet(data_key)
    plaintext_payload = f.decrypt(encrypted_payload).decode('utf-8')

    return {'plaintext': plaintext_payload}
