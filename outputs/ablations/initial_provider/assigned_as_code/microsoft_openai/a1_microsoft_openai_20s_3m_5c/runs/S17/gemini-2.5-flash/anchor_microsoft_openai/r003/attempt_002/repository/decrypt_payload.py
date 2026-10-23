from azure.keyvault.keys.crypto import EncryptionAlgorithm
from security_client import get_key_vault_cryptography_client
from security_models import DecryptionRequest, DecryptionResponse

def decrypt_payload(request: DecryptionRequest):
    if request.algorithm != 'A256GCM':
        raise ValueError("Unsupported algorithm. Only A256GCM is supported for this decryption method.")

    client = get_key_vault_cryptography_client(request.key_id)
    
    response = client.decrypt(
        EncryptionAlgorithm.a256_gcm,
        request.ciphertext,
        iv=request.iv,
        authentication_tag=request.tag
    )

    return DecryptionResponse(
        plaintext=response.plaintext,
        key_id=request.key_id,
        algorithm=request.algorithm
    )
