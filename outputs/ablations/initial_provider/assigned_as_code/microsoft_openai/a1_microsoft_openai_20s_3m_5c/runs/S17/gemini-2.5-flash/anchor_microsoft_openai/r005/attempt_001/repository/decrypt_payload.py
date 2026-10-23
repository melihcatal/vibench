from azure.keyvault.keys.crypto import EncryptionAlgorithm
from security_client import get_cryptography_client
from security_models import DecryptionRequest, DecryptionResponse

def decrypt_payload(request: DecryptionRequest) -> DecryptionResponse:
    # Azure Key Vault CryptographyClient.decrypt expects iv and authentication_tag
    # These were returned by the encrypt_payload function.
    if not request.iv or not request.tag:
        raise ValueError("IV and authentication tag are required for AES-GCM decryption.")

    client = get_cryptography_client(request.key_id)
    response = client.decrypt(
        EncryptionAlgorithm.a256_gcm, # Assuming the same algorithm as encrypt_payload
        request.ciphertext,
        iv=request.iv,
        authentication_tag=request.tag
    )
    return DecryptionResponse(
        plaintext=response.plaintext,
        key_id=request.key_id,
        algorithm="A256GCM" # Assuming the same algorithm as encrypt_payload
    )
