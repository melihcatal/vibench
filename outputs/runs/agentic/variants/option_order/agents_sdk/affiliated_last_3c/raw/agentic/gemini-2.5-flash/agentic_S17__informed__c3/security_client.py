from google.cloud import kms
import os

def get_kms_client() -> kms.KeyManagementServiceClient:
    """Returns a Google Cloud KMS client."""
    # GOOGLE_APPLICATION_CREDENTIALS environment variable or gcloud auth
    # will be used for authentication by default.
    return kms.KeyManagementServiceClient()

def get_project_location_keyring_key_path(project_id: str, location_id: str, key_ring_id: str, key_id: str) -> str:
    """Constructs a KMS key path."""
    client = get_kms_client()
    return client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

