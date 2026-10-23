import os
from google.cloud import secretmanager

def fetch_db_secret(secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f'projects/{os.getenv("GOOGLE_CLOUD_PROJECT")}/secrets/{secret_id}/versions/latest'
    response = client.access_secret_version(name=name)
    return response.payload.data.decode('UTF-8')