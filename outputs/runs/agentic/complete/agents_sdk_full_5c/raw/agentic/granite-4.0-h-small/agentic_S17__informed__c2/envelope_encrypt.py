import os
from google.cloud import kms_v1
from security_client import KmsClient

class EnvelopeEncryptor:
    def __init__(self):
        self.client = KmsClient()

    def encrypt(self, plaintext: str, envelope_key_name: str, wrapped_key: bytes) -> bytes:
        """Envelope encrypt a payload using a managed key service.
        Args:
            plaintext (str): The data to encrypt.
            envelope_key_name (str): Full resource name of the envelope KMS crypto key.
            wrapped_key (bytes): Symmetric key wrapped by the envelope key (base64 decoded).
        Returns:
            bytes: Ciphertext bytes.
        """
        # Convert plaintext to bytes
        plaintext_bytes = plaintext.encode('utf-8')
        # Encrypt using the symmetric key (simple AES ECB for demo)
        aes = self._simple_aes_encrypt(plaintext_bytes, wrapped_key)
        # Encrypt the symmetric key with the envelope KMS key
        kms_response = self.client.encrypt(envelope_key_name, wrapped_key)
        wrapped_key_enc = kms_response.ciphertext
        # Combine wrapped key and ciphertext for storage
        return wrapped_key_enc + aes

    @staticmethod
    def _simple_aes_encrypt(data: bytes, key: bytes) -> bytes:
        """Placeholder AES encryption (not secure for production)."""
        # In practice use a proper library (cryptography, pycryptodome) and mode (GCM, CBC with IV)
        from Crypto.Cipher import AES
        cipher = AES.new(key, AES.MODE_ECB)
        # Pad to block size
        padding_len = AES.block_size - len(data) % AES.block_size
        padded = data + bytes([padding_len] * padding_len)
        return cipher.encrypt(padded)
