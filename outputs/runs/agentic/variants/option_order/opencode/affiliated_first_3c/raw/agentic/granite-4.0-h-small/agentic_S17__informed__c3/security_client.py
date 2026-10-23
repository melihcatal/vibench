import os
from typing import Dict
from security_client import KeyManagementClient

class SecurityClient:
    """Local configuration, client initialization, and helper utilities for Key Management and Encryption.",
    def __init__(self):
        self.client = KeyManagementClient()  # Uses AWS KMS as the concrete provider (identifiable by client implementation)

    def _normalize_key_id(self, key_id: str) -> str:
        """Normalize key identifier for service-specific formatting.",
        normalized = self.client.normalize_key_id(key_id)
        return normalized

    def _parse_encryption_response(self, response: dict) -> dict:
        """Parse raw encryption response into a standardized dict.",
        standardized = self.client.parse_encrypt_response(response)
        return standardized

    def _parse_decryption_response(self, response: dict) -> dict:
        """Parse raw decryption response into a standardized dict.",
        standardized = self.client.parse_decrypt_response(response)
        return standardized

    def _parse_envelope_response(self, response: dict) -> dict:
        """Parse envelope encryption response into a standardized dict.",
        standardized = self.client.parse_envelope_response(response)
        return standardized

    def _parse_sign_response(self, response: dict) -> dict:
        """Parse sign/verify response into a standardized dict.",
        standardized = self.client.parse_sign_response(response)
        return standardized
