import json
import os

from security_client import get_gcp_secret_manager_client
from security_models import SecretPayload, SecretResponse

def fetch_db_secret(payload: SecretPayload, project_id: str) -> SecretResponse:
    client = get_gcp_secret_manager_client()
    name = f"projects/{project_id}/secrets/{payload.secret_id}/versions/{payload.version}"
    response = client.access_secret_version(request={"name": name})
    db_secret_value = response.payload.data.decode("utf-8")
    
    if payload.key_field:
        db_secret_value = json.loads(db_secret_value)[payload.key_field]
    
    return SecretResponse(value=db_secret_value, secret_id=payload.secret_id, version=payload.version)
