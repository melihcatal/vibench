import json
import os
from google.cloud import secretmanager

def parse_json_secret(secret_name: str) -> dict:
    """Retrieve a secret from Google Secret Manager and parse it as JSON.
    Raises ValueError if the secret content is not valid JSON.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{os.getenv('GCP_PROJECT')}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(name=name)
    data = response.payload.data.decode('UTF-8')
    return json.loads(data)
