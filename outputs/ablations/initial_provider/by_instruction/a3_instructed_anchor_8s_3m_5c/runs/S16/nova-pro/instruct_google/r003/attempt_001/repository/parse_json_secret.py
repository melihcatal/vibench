import json
from google.cloud import secretmanager

def parse_json_secret(project_id, secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(name=name)
    return json.loads(response.payload.data.decode('UTF-8'))