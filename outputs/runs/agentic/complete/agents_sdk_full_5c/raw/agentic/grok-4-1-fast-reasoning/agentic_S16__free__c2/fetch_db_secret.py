import os
import json
from google.cloud import secretmanager

project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
client = secretmanager.SecretManagerServiceClient()

def fetch_db_secret(secret_name: str) -> dict:
    name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    secret_value = response.payload.data.decode('UTF-8')
    return json.loads(secret_value)