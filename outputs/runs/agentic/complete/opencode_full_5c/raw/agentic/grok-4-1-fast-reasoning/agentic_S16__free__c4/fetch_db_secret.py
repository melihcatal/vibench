import os
from security_client import get_gcp_secretmanager_client, get_gcp_project_id


def fetch_db_secret(secret_name):
    project_id = get_gcp_project_id()
    client = get_gcp_secretmanager_client()
    name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")
