from security_client import get_key_vault_cryptography_client
from security_models import DecryptionRequest, DecryptionResponse
from azure.keyvault.keys.crypto import EncryptionAlgorithm

def decrypt_payload(payload: dict) -> DecryptionResponse:
    key_id = payload['key_id']
    ciphertext = payload['ciphertext']
    iv = payload['iv']
    tag = payload['tag']
    algorithm = payload.get('algorithm', 'A256GCM')

    if algorithm.upper() != 'A256GCM':
        raise ValueError("Unsupported decryption algorithm. Only A256GCM is supported.")

    crypto_client = get_key_vault_cryptography_client(key_id)
    
    # The decrypt method expects ciphertext, iv, and authentication_tag for AES-GCM.
    response = crypto_client.decrypt(
        EncryptionAlgorithm.a256_gcm,
        ciphertext,
        iv=iv,
        authentication_tag=tag
    )

    return DecryptionResponse(
        plaintext=response.plaintext,
        key_id=response.key_id
    )
