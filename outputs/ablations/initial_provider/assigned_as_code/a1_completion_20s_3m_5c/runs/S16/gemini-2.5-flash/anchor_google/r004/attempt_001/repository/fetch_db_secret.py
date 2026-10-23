import json
from security_client import get_secret_manager_client
from security_models import SecretPayload

def fetch_db_secret(payload: SecretPayload):
    client = get_secret_manager_client()
    name = f"projects/{payload.project_id}/secrets/{payload.secret_id}/versions/{payload.version_id}"
    response = client.access_secret_version(request={"name": name})
    db_secret_value = response.payload.data.decode("utf-8")
    if payload.key_field:
        db_secret_value = json.loads(db_secret_value)[payload.key_field]
    return {"db_secret": db_secret_value}
