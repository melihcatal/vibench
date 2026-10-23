from security_client import get_gcp_secretmanager_client, get_gcp_project, get_env
from security_models import SecretResponse

def fetch_db_secret(secret_id: str = None) -> SecretResponse:
    if secret_id is None:
        secret_id = get_env('DB_SECRET_ID')
        if not secret_id:
            raise ValueError('DB_SECRET_ID environment variable or secret_id argument required')
    project = get_gcp_project()
    name = f'projects/{project}/secrets/{secret_id}/versions/latest'
    client = get_gcp_secretmanager_client()
    response = client.access_secret_version(request={'name': name})
    value = response.payload.data.decode('UTF-8')
    version_id = response.name.split('/')[-1]
    return {
        'name': secret_id,
        'value': value,
        'version_id': version_id
    }