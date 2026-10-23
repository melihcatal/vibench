from google.cloud import kms_v1

class SecurityClient:
    """
    Provides local configuration and client helper utilities for Key Management and Encryption.
    """

    def __init__(self, project_id: str, location: str, key_ring_id: str, key_id: str):
        self.project_id = project_id
        self.location = location
        self.key_ring_id = key_ring_id
        self.key_id = key_id
        self.kms_client = self._get_kms_client()

    def _get_kms_client(self):
        """
        Initializes and returns a Google Cloud KMS client.
        """
        return kms_v1.KeyManagementServiceClient()

    def get_key_name(self) -> str:
        """
        Constructs and returns the full KMS key name.
        """
        return self.kms_client.crypto_key_path(
            self.project_id, self.location, self.key_ring_id, self.key_id
        )
