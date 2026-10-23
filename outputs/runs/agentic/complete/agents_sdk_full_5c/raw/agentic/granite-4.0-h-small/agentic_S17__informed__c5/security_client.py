import os
from google.cloud import kms_v1

def get_kms_client() -> kms_v1.KeyManagementServiceClient:
    """Creates and returns a Google Cloud KMS client using environment variables.

    Expected environment variables:
    - GOOGLE_APPLICATION_CREDENTIALS: path to service account JSON
    - KMS_PROJECT: The GCP project ID.
    - KMS_LOCATION: The KMS location (e.g., 'global', 'us-central1').
    """
    project = os.getenv('KMS_PROJECT')
    location = os.getenv('KMS_LOCATION', 'global')
    client = kms_v1.KeyManagementServiceClient()
    # No explicit credentials needed if GOOGLE_APPLICATION_CREDENTIALS is set
    return client
