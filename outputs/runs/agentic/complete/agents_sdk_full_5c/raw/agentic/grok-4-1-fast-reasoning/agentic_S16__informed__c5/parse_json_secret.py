from google.cloud import secretmanager
import os
from security_client import parse_json_secret

def fetch_parse_json_secret(project_id: str = None, secret_id: str = None, version_id: str = 'latest') -> dict:
    if project_id is None:
        project_id = os.getenv('GOOGLE_CLOUD_PROJECT', 'my-project')
    if secret_id is None:
        secret_id = os.getenv('JSON_SECRET_ID', 'my-config')
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("UTF-8")
    return parse_json_secret(payload)