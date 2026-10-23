import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.cryptography import CryptographyClient
from security_models import EncryptionRequest, EncryptionResponse, DecryptionRequest, DecryptionResponse, EnvelopeEncryptionRequest, EnvelopeEncryptionResponse, EnvelopeDecryptionRequest, EnvelopeDecryptionResponse, SignRequest, SignResponse, VerifyRequest, VerifyResponse

class AzureKeyVaultSecurityClient:
    def __init__(self, key_vault_url: str):
        self.key_vault_url = key_vault_url
        self.credential = DefaultAzureCredential()

    def _get_cryptography_client(self, key_id: str):
        return CryptographyClient(key_id, self.credential)

    def encrypt(self, request: EncryptionRequest) -> EncryptionResponse:
        key_id = f"{request.key_vault_url}/keys/{request.key_name}"
        crypto_client = self._get_cryptography_client(key_id)
        
        # Azure Key Vault's encrypt operation expects bytes
        plaintext_bytes = request.plaintext.encode('utf-8')
        result = crypto_client.encrypt("RSA-OAEP", plaintext_bytes)
        
        return EncryptionResponse(
            ciphertext=result.ciphertext.hex(), # Convert bytes to hex string for easier storage/transfer
            key_id=result.key_id,
            algorithm="RSA-OAEP"
        )

    def decrypt(self, request: DecryptionRequest) -> DecryptionResponse:
        crypto_client = self._get_cryptography_client(request.key_id)
        
        # Azure Key Vault's decrypt operation expects bytes
        ciphertext_bytes = bytes.fromhex(request.ciphertext) # Convert hex string back to bytes
        result = crypto_client.decrypt(request.algorithm, ciphertext_bytes)
        
        return DecryptionResponse(
            plaintext=result.plaintext.decode('utf-8') # Decode bytes back to string
        )

    def envelope_encrypt(self, request: EnvelopeEncryptionRequest) -> EnvelopeEncryptionResponse:
        key_id = f"{request.key_vault_url}/keys/{request.key_name}"
        crypto_client = self._get_cryptography_client(key_id)

        plaintext_bytes = request.plaintext.encode('utf-8')
        result = crypto_client.encrypt_a_new_key("A128CBC", plaintext_bytes) # Using A128CBC as an example for data encryption key
        
        return EnvelopeEncryptionResponse(
            ciphertext=result.ciphertext.hex(),
            wrapped_key=result.wrapped_key.hex(),
            key_id=result.key_id,
            algorithm="A128CBC"
        )

    def envelope_decrypt(self, request: EnvelopeDecryptionRequest) -> EnvelopeDecryptionResponse:
        crypto_client = self._get_cryptography_client(request.key_id)
        
        ciphertext_bytes = bytes.fromhex(request.ciphertext)
        wrapped_key_bytes = bytes.fromhex(request.wrapped_key)
        
        result = crypto_client.decrypt_a_key("A128CBC", ciphertext_bytes, wrapped_key_bytes) # Assuming A128CBC as the original algorithm
        
        return EnvelopeDecryptionResponse(
            plaintext=result.plaintext.decode('utf-8')
        )

    def sign(self, request: SignRequest) -> SignResponse:
        key_id = f"{request.key_vault_url}/keys/{request.key_name}"
        crypto_client = self._get_cryptography_client(key_id)
        
        result = crypto_client.sign(request.algorithm, request.digest)
        
        return SignResponse(
            signature=result.signature,
            key_id=result.key_id
        )

    def verify(self, request: VerifyRequest) -> VerifyResponse:
        key_id = f"{request.key_vault_url}/keys/{request.key_name}"
        crypto_client = self._get_cryptography_client(key_id)
        
        result = crypto_client.verify(request.algorithm, request.digest, request.signature)
        
        return VerifyResponse(
            is_valid=result.is_valid
        )
