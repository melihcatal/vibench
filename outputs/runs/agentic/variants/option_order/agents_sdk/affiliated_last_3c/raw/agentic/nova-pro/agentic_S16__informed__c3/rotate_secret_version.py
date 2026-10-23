import os
from google.cloud import secretmanager

def rotate_secret_version(secret_id, version):
    client = secretmanager.SecretManagerServiceClient()
    name = f'projects/{os.getenv("GOOGLE_CLOUD_PROJECT")}/secrets/{secret_id}/versions/{version}'
    response = client.access_secret_version(name=name)
    return response.payload.data.decode('UTF-8')