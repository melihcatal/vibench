import json
from security_client import get_google_secret_manager_client
from security_models import Secret

def parse_json_secret(project_id: str, secret_id: str, version_id: str = "latest") -> dict:
    client = get_google_secret_manager_client()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    
    response = client.access_secret_version(name=name)
    payload = response.payload.data.decode('UTF-8')
    
    secret = Secret(name=secret_id, value=payload)
    return json.loads(secret.value)

