from google.cloud import kms_v1
import os

def get_kms_client():
    """Returns a Google Cloud KMS client."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or other authentication methods are configured for the Google Cloud client library.
    return kms_v1.KeyManagementServiceClient()
