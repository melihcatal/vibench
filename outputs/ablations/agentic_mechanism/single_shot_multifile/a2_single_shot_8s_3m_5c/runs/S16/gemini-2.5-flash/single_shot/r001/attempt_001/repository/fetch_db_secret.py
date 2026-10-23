import json
from security_client import SecurityClients
from security_models import SecretData
from google.api_core.exceptions import NotFound

def fetch_db_secret(project_id: str, secret_id: str, version_id: str = "latest") -> SecretData:
    client = SecurityClients.get_google_secret_manager_client()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    try:
        response = client.access_secret_version(request={"name": name})
        payload = response.payload.data.decode("UTF-8")
        
        db_secret_value = None
        try:
            secret_dict = json.loads(payload)
            db_secret_value = json.dumps(secret_dict)
        except json.JSONDecodeError:
            db_secret_value = payload

        return SecretData(name=secret_id, value=db_secret_value, version=version_id)
    except NotFound:
        raise ValueError(f"Secret '{secret_id}' with version '{version_id}' not found in project '{project_id}'.")
    except Exception as e:
        raise RuntimeError(f"Error fetching database secret '{secret_id}': {e}")