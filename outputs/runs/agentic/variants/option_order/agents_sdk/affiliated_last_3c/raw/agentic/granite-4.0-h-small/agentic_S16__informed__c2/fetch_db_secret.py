import os
from google.cloud import secretmanager
from security_client import get_project_id

def fetch_db_secret():
    project_id = get_project_id()
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/DB-CONNECTION/versions/latest"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode('UTF-8')
