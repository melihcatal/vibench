from google.cloud import kms
import os


def get_kms_client():
    """
    Initializes and returns a Google Cloud KMS client.
    
    Returns:
        A configured Google Cloud KMS client.
    """
    # Google Cloud KMS-specific client initialization
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
    
    return kms.KeyManagementServiceClient()