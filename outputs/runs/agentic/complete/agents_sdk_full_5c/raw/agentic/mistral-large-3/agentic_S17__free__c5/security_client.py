import os
from google.cloud import kms
from google.api_core.exceptions import GoogleAPICallError
from typing import Optional

class KMSConfig:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        self.location_id = os.getenv("KMS_LOCATION", "global")
        self.key_ring_id = os.getenv("KMS_KEY_RING")
        self.key_id = os.getenv("KMS_KEY_ID")

def get_kms_client() -> kms.KeyManagementServiceClient:
    return kms.KeyManagementServiceClient()