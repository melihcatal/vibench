import json
from security_client import SecretManagerClient
from security_models import JsonSecretPayload, SecretOutput

def parse_json_secret(payload: JsonSecretPayload) -> SecretOutput:
    client = SecretManagerClient()
    secret_value = client.access_secret_version(
        project_id=payload.project_id,
        secret_id=payload.secret_id,
        version=payload.version
    )
    parsed_json = json.loads(secret_value)
    
    if payload.key_field:
        parsed_json = parsed_json.get(payload.key_field)

    return SecretOutput(secret_id=payload.secret_id, value=parsed_json)
