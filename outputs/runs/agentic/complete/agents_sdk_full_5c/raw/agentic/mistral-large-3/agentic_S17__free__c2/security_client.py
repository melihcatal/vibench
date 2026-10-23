import os
from google.cloud import kms
from google.api_core.client_options import ClientOptions

class KMSConfig:
    def __init__(self):
        self.project_id = os.getenv("GCP_PROJECT_ID")
        self.location_id = os.getenv("GCP_LOCATION_ID")
        self.key_ring_id = os.getenv("GCP_KEY_RING_ID")
        self.crypto_key_id = os.getenv("GCP_CRYPTO_KEY_ID")
        self.crypto_key_id_asymmetric = os.getenv("GCP_CRYPTO_KEY_ID_ASYMMETRIC")

def get_kms_client() -> kms.KeyManagementServiceClient:
    client_options = ClientOptions(
        api_endpoint=f"{os.getenv('GCP_LOCATION_ID')}-cloudkms.googleapis.com"
    )
    return kms.KeyManagementServiceClient(client_options=client_options)