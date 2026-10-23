import os
from google.cloud import kms_v1

def get_kms_client():
    """Provides a configured Google Cloud KMS client."""
    # Credentials will be automatically picked up from GOOGLE_APPLICATION_CREDENTIALS
    # environment variable or metadata server.
    return kms_v1.KeyManagementServiceClient()
