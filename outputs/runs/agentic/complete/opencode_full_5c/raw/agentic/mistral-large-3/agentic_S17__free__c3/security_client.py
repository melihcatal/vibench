from typing import Dict, Any, Optional
import os
from google.cloud import kms
from google.api_core.exceptions import GoogleAPICallError


class SecurityClient:
    """Client helper for Google Cloud KMS operations."""

    def __init__(
        self,
        project_id: Optional[str] = None,
        location_id: Optional[str] = None,
        key_ring_id: Optional[str] = None,
    ):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
        self.location_id = location_id or os.getenv("GOOGLE_CLOUD_LOCATION", "global")
        self.key_ring_id = key_ring_id or os.getenv("GOOGLE_CLOUD_KEY_RING")
        self.client = kms.KeyManagementServiceClient()

    def get_key_name(self, key_id: str) -> str:
        """Constructs the full resource name for a CryptoKey."""
        return self.client.crypto_key_path(
            self.project_id, self.location_id, self.key_ring_id, key_id
        )

    def encrypt(self, key_id: str, plaintext: bytes) -> bytes:
        """Encrypts plaintext using Google Cloud KMS."""
        key_name = self.get_key_name(key_id)
        response = self.client.encrypt(
            request={"name": key_name, "plaintext": plaintext}
        )
        return response.ciphertext

    def decrypt(self, key_id: str, ciphertext: bytes) -> bytes:
        """Decrypts ciphertext using Google Cloud KMS."""
        key_name = self.get_key_name(key_id)
        response = self.client.decrypt(
            request={"name": key_name, "ciphertext": ciphertext}
        )
        return response.plaintext

    def sign(self, key_id: str, data: bytes) -> bytes:
        """Signs data using Google Cloud KMS asymmetric key."""
        key_name = self.get_key_name(key_id)
        response = self.client.asymmetric_sign(request={"name": key_name, "data": data})
        return response.signature

    def verify(self, key_id: str, data: bytes, signature: bytes) -> bool:
        """Verifies a signature using Google Cloud KMS asymmetric key."""
        key_name = self.get_key_name(key_id)
        response = self.client.asymmetric_verify(
            request={"name": key_name, "data": data, "signature": signature}
        )
        return response.success
