from google.cloud import kms
import os

def get_kms_client() -> kms.KeyManagementServiceClient:
    """Initializes and returns a Google Cloud KMS client."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or authenticated via `gcloud auth application-default login`
    return kms.KeyManagementServiceClient()

# Example of how to get a specific KMS location client if needed (less common)
# from google.api_core.client_options import ClientOptions
# def get_kms_regional_client(location: str) -> kms.KeyManagementServiceClient:
#     client_options = ClientOptions(api_endpoint=f"{location}-kms.googleapis.com")
#     return kms.KeyManagementServiceClient(client_options=client_options)
