import os
from google.cloud import secretmanager

class SecurityClient:
    def __init__(self):
        self.client = secretmanager.SecretManagerServiceClient()

    def get_secret(self, secret_id):
        name = f'projects/{os.getenv("GOOGLE_CLOUD_PROJECT")}/secrets/{secret_id}/versions/latest'
        response = self.client.access_secret_version(name=name)
        return response.payload.data.decode('UTF-8')