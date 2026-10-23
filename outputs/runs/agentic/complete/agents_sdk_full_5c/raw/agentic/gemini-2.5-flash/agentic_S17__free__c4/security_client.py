
"""
security_client.py - Provide local configuration and client helper utilities for Key Management and Encryption.
"""

from google.cloud import kms_v1

class KmsClient:
    def __init__(self):
        self.client = kms_v1.KeyManagementServiceClient()
        # The KMS API hostname is kms.googleapis.com

    def get_key_name(self, project_id: str, location_id: str, key_ring_id: str, key_id: str) -> str:
        return self.client.key_path(project_id, location_id, key_ring_id, key_id)

    def get_key_version_name(self, project_id: str, location_id: str, key_ring_id: str, key_id: str, version_id: str) -> str:
        return self.client.crypto_key_version_path(project_id, location_id, key_ring_id, key_id, version_id)

