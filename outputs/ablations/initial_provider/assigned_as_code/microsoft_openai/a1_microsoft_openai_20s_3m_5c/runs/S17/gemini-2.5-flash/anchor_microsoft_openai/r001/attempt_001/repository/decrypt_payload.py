from security_client import get_cryptography_client
from security_models import deserialize_payload
from azure.keyvault.keys.crypto import EncryptionAlgorithm


def decrypt_payload(payload):
    # Reconstruct the key_id from the original encryption response if not directly provided
    key_id = payload.get('key_id')
    if not key_id:
        raise ValueError("Key ID is required for decryption.")

    client = get_cryptography_client(key_id)
    
    # The algorithm from encrypt_payload.py is A256GCM
    # Ensure the correct algorithm and parameters are passed
    response = client.decrypt(
        EncryptionAlgorithm.a256_gcm,
        payload['ciphertext'],
        iv=payload['iv'],
        authentication_tag=payload['tag']
    )
    return {'plaintext': response.plaintext.decode('utf-8'), 'key_id': response.key_id}
