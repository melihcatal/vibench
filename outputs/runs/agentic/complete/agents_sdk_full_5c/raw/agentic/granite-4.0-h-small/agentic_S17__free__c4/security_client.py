import os
from google.cloud import kms_v1, storage

def get_kms_client() -> kms_v1.KeyManagementServiceClient:
    """Return a Google Cloud KMS client, using default credentials and environment settings."""
    return kms_v1.KeyManagementServiceClient()

def get_storage_client() -> storage.Client:
    """Return a Google Cloud Storage client, using default credentials and environment settings."""
    return storage.Client()

# Optional: centralized config loader (could read from env or secret manager)
def load_config() -> dict:
    """Load configuration for KMS and storage resources."""
    project_id = os.getenv('CLOUD_PROJECT_ID')
    location = os.getenv('CLOUD_KMS_LOCATION', 'global')
    key_ring = os.getenv('CLOUD_KMS_KEY_RING')
    return {
        'project_id': project_id,
        'location': location,
        'key_ring': key_ring,
    }
