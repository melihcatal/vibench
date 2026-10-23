import os
from security_client import get_google_secret_client
from security_models import DbCredentials

def fetch_db_secret(secret_id: str) -> DbCredentials:
    client = get_google_secret_client()
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    if not project_id:
        raise ValueError('GOOGLE_CLOUD_PROJECT must be set')
    name = f'projects/{project_id}/secrets/{secret_id}/versions/latest'
    response = client.access_secret_version(request={'name': name})
    secret_string = response.payload.data.decode('UTF-8')
    db_creds = DbCredentials.model_validate_json(secret_string)
    return db_creds
