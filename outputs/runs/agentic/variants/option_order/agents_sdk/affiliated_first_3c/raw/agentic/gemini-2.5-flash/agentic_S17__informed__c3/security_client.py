import os
from google.cloud import kms_v1

class KMSClient:
    def __init__(self):
        self.project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
        self.client = kms_v1.KeyManagementServiceClient()

    def get_client(self):
        return self.client
