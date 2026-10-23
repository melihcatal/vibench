from google.cloud import kms_v1
import os


def get_kms_client():
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or that the application is running in an environment with default credentials.
    # For local development, set GOOGLE_APPLICATION_CREDENTIALS to the path of your service account key file.
    # Example: os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/path/to/your/key.json'
    return kms_v1.KeyManagementServiceClient()
