import json
from security_client import SecretManagerClient
from security_models import DbSecretPayload, SecretOutput

def fetch_db_secret(payload: DbSecretPayload) -> SecretOutput:
    client = SecretManagerClient()
    secret_value = client.access_secret_version(
        project_id=payload.project_id,
        secret_id=payload.secret_id,
        version=payload.version
    )
    if payload.key_field:
        secret_value = json.loads(secret_value)[payload.key_field]
    
    return SecretOutput(secret_id=payload.secret_id, value=secret_value)
