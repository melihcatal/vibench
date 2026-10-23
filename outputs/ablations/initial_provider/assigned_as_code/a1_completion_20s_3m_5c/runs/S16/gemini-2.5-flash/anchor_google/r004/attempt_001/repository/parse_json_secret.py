import json
from security_client import get_secret_manager_client
from security_models import SecretPayload

def parse_json_secret(payload: SecretPayload):
    client = get_secret_manager_client()
    name = f"projects/{payload.project_id}/secrets/{payload.secret_id}/versions/{payload.version_id}"
    response = client.access_secret_version(request={"name": name})
    secret_value = response.payload.data.decode("utf-8")
    parsed_secret = json.loads(secret_value)
    if payload.key_field:
        return {payload.key_field: parsed_secret.get(payload.key_field)}
    return {"parsed_secret": parsed_secret}
