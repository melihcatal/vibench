import json
from security_client import get_secret_manager_client
from security_models import SecretPayload

def parse_json_secret(project_id: str, secret_id: str, version_id: str = "latest") -> dict:
    client = get_secret_manager_client()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    json_secret_data = response.payload.data.decode("UTF-8")
    return json.loads(json_secret_data)
