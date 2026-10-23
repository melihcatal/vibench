import os
from google.cloud import kms_v1


class KmsClient:
    def __init__(self):
        self.client = kms_v1.KeyManagementServiceClient()
        # GOOGLE_APPLICATION_CREDENTIALS environment variable is expected for authentication
        # Key format: projects/PROJECT_ID/locations/LOCATION_ID/keyRings/KEY_RING_ID/cryptoKeys/CRYPTO_KEY_ID

    def get_client(self):
        return self.client
