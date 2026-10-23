import os
from google.cloud import secretmanager

def get_secret_client():
    return secretmanager.SecretManagerServiceClient()

def get_secret_name(project_id, secret_id, version_id='latest'):
    client = get_secret_client()
    return client.secret_version_path(project_id, secret_id, version_id)