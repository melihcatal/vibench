from google.cloud import secretmanager
import json
import os

from security_models import JsonSecretResponse

def parse_json_secret(secret_name: str, project_id: str) -> JsonSecretResponse:
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    
    response = client.access_secret_version(request={"name": name})
    secret_value = response.payload.data.decode("UTF-8")
    
    parsed = json.loads(secret_value)
    return JsonSecretResponse(
        name=secret_name,
        value=parsed,
        version=response.name.split('/')[-2]
    )