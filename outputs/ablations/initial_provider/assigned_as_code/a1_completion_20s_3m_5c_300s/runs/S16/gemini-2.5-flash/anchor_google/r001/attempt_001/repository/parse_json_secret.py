import json
from security_client import SecretManagerClient
from security_models import SecretPayload, SecretResponse

def parse_json_secret(payload: SecretPayload, config: dict) -> SecretResponse:
    client = SecretManagerClient()
    project_id = payload.project_id or config.get("project_id")
    if not project_id:
        raise ValueError("Project ID must be provided in payload or config.")

    secret_name = client.get_secret_version_name(
        project_id=project_id,
        secret_id=payload.secret_id,
        version_id=payload.version_id
    )
    response = client.access_secret_version(secret_name)
    secret_data_raw = response.payload.data.decode("utf-8")
    
    parsed_data = json.loads(secret_data_raw)
    if payload.key_field:
        parsed_data = parsed_data.get(payload.key_field)

    return SecretResponse(
        secret_id=payload.secret_id,
        version_id=payload.version_id, # This might not be the actual version, but the requested one
        data=json.dumps(parsed_data) if isinstance(parsed_data, (dict, list)) else str(parsed_data)
    )
