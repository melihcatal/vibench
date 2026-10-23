import os
from google.cloud import kms_v1
from typing import Optional

class KMSClient:
    """Thin wrapper around Google Cloud KMS providing unified encrypt/decrypt/sign/verify methods."""
    
    def __init__(self):
        # Uses application default credentials configured via GOOGLE_APPLICATION_CREDENTIALS env var
        self.client = kms_v1.KeyManagementServiceClient()
        self.location = os.getenv('KMS_LOCATION', 'global')
        
    def encrypt(self, key_name: str, plaintext_bytes: bytes) -> bytes:
        """Call KMS Encrypt API."""
        crypto_key_path = f"projects/{self.project_id}/locations/{self.location}/keyRings/{self.key_ring}/cryptoKeys/{key_name.split('/')[-1]}"
        response = self.client.encrypt(name=crypto_key_path, plaintext=plaintext_bytes)
        return response.ciphertext
    
    def decrypt(self, key_name: str, ciphertext_bytes: bytes) -> bytes:
        """Call KMS Decrypt API."""
        crypto_key_path = f"projects/{self.project_id}/locations/{self.location}/keyRings/{self.key_ring}/cryptoKeys/{key_name.split('/')[-1]}"
        response = self.client.decrypt(name=crypto_key_path, ciphertext_blob=ciphertext_bytes)
        return response.plaintext
    
    def sign(self, key_name: str, data: bytes) -> bytes:
        """Create a digital signature using an asymmetric CryptoKey."""
        crypto_key_path = f"projects/{self.project_id}/locations/{self.location}/keyRings/{self.key_ring}/cryptoKeys/{key_name.split('/')[-1]}"
        response = self.client.asymmetric_sign(name=crypto_key_path, digest={'bytes': data})
        return response.signature
    
    def verify(self, key_name: str, data: bytes, signature_bytes: bytes) -> bool:
        """Verify an asymmetric signature."""
        crypto_key_path = f"projects/{self.project_id}/locations/{self.location}/keyRings/{self.key_ring}/cryptoKeys/{key_name.split('/')[-1]}"
        try:
            self.client.asymmetric_verify(
                name=crypto_key_path,
                digest={'bytes': data},
                signature=signature_bytes
            )
            return True
        except Exception:
            return False
    
    @property
    def project_id(self):
        return os.getenv('KMS_PROJECT_ID')
    
    @property
    def key_ring(self):
        return os.getenv('KMS_KEY_RING')
