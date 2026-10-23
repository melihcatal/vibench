from google.cloud import secretmanager

def get_secret_client(config=None):
    config = config or {}
    return secretmanager.SecretManagerServiceClient()

def get_secret_name(project_id, secret_id, version='latest'):
    return f'projects/{project_id}/secrets/{secret_id}/versions/{version}'